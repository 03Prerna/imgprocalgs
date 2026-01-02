from imgprocalgs.algorithms.base import ImageProcessingAlgorithm
import os
from PIL import ImageEnhance, ImageOps

class GenAIAlgorithm(ImageProcessingAlgorithm):
    def __init__(self, image_path, api_key=None):
        super().__init__(image_path)
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.environ.get("GENAI_API_KEY")

    def call_api(self, prompt):
        print(f"Processing with prompt: {prompt}")

class GenAIImageEnhancer(GenAIAlgorithm):
    def process(self, dest_path, user_text=None):
        prompt = "Enhance image"
        if user_text:
            prompt = prompt + " " + user_text
        
        self.call_api(prompt)
        
        enhancer = ImageEnhance.Sharpness(self.image.image)
        img = enhancer.enhance(2.0)
        
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        
        img.save(dest_path)

class GenAIGhibliConverter(GenAIAlgorithm):
    def process(self, dest_path, user_text=None):
        prompt = "Ghibli style"
        if user_text:
            prompt = prompt + " " + user_text
            
        self.call_api(prompt)
        
        enhancer = ImageEnhance.Color(self.image.image)
        img = enhancer.enhance(1.5)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        img = ImageOps.posterize(img, 2)
        
        img.save(dest_path)
