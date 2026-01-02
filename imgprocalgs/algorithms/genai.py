from imgprocalgs.algorithms.base import ImageProcessingAlgorithm
import os
import google.generativeai as genai
from PIL import ImageEnhance, ImageOps, Image
import io
import time

class GenAIAlgorithm(ImageProcessingAlgorithm):
    def __init__(self, image_path, api_key=None):
        super().__init__(image_path)
        self.api_key = api_key or os.environ.get("GENAI_API_KEY")
        
        if self.api_key:
            genai.configure(api_key=self.api_key)

    def call_api(self, prompt):
        print(f"Calling Gemini API with prompt: {prompt}")
        time.sleep(35) # Wait 35s to respect free tier rate limits
        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content([prompt, self.image.image])
            print("Gemini API Response:", response.text)
            return response.text
        except Exception as e:
            print(f"Error calling API: {e}")
            return None

class GenAIImageEnhancer(GenAIAlgorithm):
    def process(self, dest_path, user_text=None):
        prompt = "Analyze this image and suggest 3 single-word parameters to improve it (e.g. sharpness, contrast). Just list them."
        if user_text:
            prompt = f"{prompt} User also asked: {user_text}"
        
        self.call_api(prompt)
        
        print("Applying enhancement filters...")
        enhancer = ImageEnhance.Sharpness(self.image.image)
        img = enhancer.enhance(2.0)
        
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        
        img.save(dest_path)

class GenAIGhibliConverter(GenAIAlgorithm):
    def process(self, dest_path, user_text=None):
        print("Generating Ghibli style image using GenAI...")
        
        description_prompt = "Describe this image in detail. Focus on the scene, subjects, colors, and composition."
        description = self.call_api(description_prompt) or ""
        
        gen_prompt = f"Create a Studio Ghibli style illustration. {user_text or ''} Scene description: {description}"
        print(f"Generating image with prompt: {gen_prompt[:100]}...")
        
        try:
            self._generate_and_save_image(gen_prompt, dest_path)
        except Exception as e:
            print(f"Error generating image: {e}")
            print("Falling back to filter-based approach...")
            self._apply_fallback_filters(dest_path)

    def _generate_and_save_image(self, prompt, dest_path):
        print("Waiting 35s before image generation to respect rate limits...")
        time.sleep(35)
        model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')
        response = model.generate_content(prompt)
        
        if self._save_image_from_response(response, dest_path):
            print(f"Successfully saved Ghibli image to {dest_path}")
            return

        raise ValueError("No image data found in GenAI response.")

    def _save_image_from_response(self, response, dest_path):
        if response.parts:
            for part in response.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    return self._save_inline_data(part.inline_data, dest_path)
        
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    return self._save_inline_data(part.inline_data, dest_path)
        
        return False

    def _save_inline_data(self, inline_data, dest_path):
        img = Image.open(io.BytesIO(inline_data.data))
        img.save(dest_path)
        return True

    def _apply_fallback_filters(self, dest_path):
        enhancer = ImageEnhance.Color(self.image.image)
        img = enhancer.enhance(1.5)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        img = ImageOps.posterize(img, 2)
        img.save(dest_path)
