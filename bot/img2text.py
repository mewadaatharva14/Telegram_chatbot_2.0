
from transformers import pipeline
from PIL import Image

captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

def caption_image(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        result = captioner(image)
        return result[0]['generated_text']
    except Exception as e:
        return f"Error generating caption: {e}"
