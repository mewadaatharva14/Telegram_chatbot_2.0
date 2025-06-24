
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import os

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    use_auth_token=os.getenv("HF_TOKEN")
)
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

def generate_image(prompt, output_path="generated_image.png"):
    try:
        image = pipe(prompt).images[0]
        image.save(output_path)
        return output_path
    except Exception as e:
        print(f"Image generation failed: {e}")
        return None
