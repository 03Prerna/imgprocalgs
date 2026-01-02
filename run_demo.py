from imgprocalgs.algorithms.genai import GenAIImageEnhancer, GenAIGhibliConverter
import os

def main():
    api_key = "AIzaSyBf1KkfOPNTo3KX1tbQ52xKn_Xz7VCsUUg"
    image_path = r"C:\aguken_assighnment\imgprocalgs\tests\data\lena.jpg"
    
    if not os.path.exists(image_path):
        print(f"Image not found at {image_path}")
        return

    print(f"Processing Image: {image_path}")
    
    enhanced_path = "output_enhanced.png"
    ghibli_path = "output_ghibli.png"

    print("Running Enhancer...")
    try:
        enhancer = GenAIImageEnhancer(image_path, api_key=api_key)
        enhancer.process(enhanced_path, user_text="Make it ultra HD")
        print(f"Enhanced saved to: {enhanced_path}")
    except Exception as e:
        print(f"Enhancer failed: {e}")

    print("Running Ghibli Converter...")
    try:
        converter = GenAIGhibliConverter(image_path, api_key=api_key)
        converter.process(ghibli_path, user_text="Spirited Away vibes")
        print(f"Ghibli saved to: {ghibli_path}")
    except Exception as e:
        print(f"Converter failed: {e}")

if __name__ == "__main__":
    main()
