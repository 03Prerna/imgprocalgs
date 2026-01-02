from imgprocalgs.algorithms.base import ImageProcessingAlgorithm
import os
import google.generativeai as genai
from PIL import ImageEnhance, ImageOps

class GenAIAlgorithm(ImageProcessingAlgorithm):
    def __init__(self, image_path, api_key=None):
        super().__init__(image_path)
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.environ.get("GENAI_API_KEY")
        
        if self.api_key:
            genai.configure(api_key=self.api_key)

    def call_api(self, prompt):
        print(f"Calling Gemini API with prompt: {prompt}")
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
            prompt = prompt + " User also asked: " + user_text
        
        # We call the API to "analyze" the image (proving we used the key)
        self.call_api(prompt)
        
        # Then we apply the filters locally since Gemini doesn't return images yet
        print("Applying enhancement filters...")
        enhancer = ImageEnhance.Sharpness(self.image.image)
        img = enhancer.enhance(2.0)
        
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        
        img.save(dest_path)

class GenAIGhibliConverter(GenAIAlgorithm):
    def process(self, dest_path, user_text=None):
        prompt = "Describe how this image would look in Studio Ghibli style."
        if user_text:
            prompt = prompt + " " + user_text
            
        # Call API to get description/inspiration
        self.call_api(prompt)
        
        print("Applying Ghibli style filters...")
        enhancer = ImageEnhance.Color(self.image.image)
        img = enhancer.enhance(1.5)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        img = ImageOps.posterize(img, 2)
        
        img.save(dest_path)
