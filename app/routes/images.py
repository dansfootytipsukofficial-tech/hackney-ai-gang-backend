from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class ImageRequest(BaseModel):
    prompt: str
    size: str = "1024x1024"
    quality: str = "standard"
    n: int = 1

class ImageResponse(BaseModel):
    images: list[str]

@router.post("/images/generate", response_model=ImageResponse)
async def generate_image(request: ImageRequest):
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.images.generate(
            model="dall-e-3",
            prompt=request.prompt,
            size=request.size,
            quality=request.quality,
            n=request.n,
        )

        image_urls = [image.url for image in response.data]

        return ImageResponse(images=image_urls)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation error: {str(e)}")