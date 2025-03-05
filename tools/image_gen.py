# tools/image_gen.py
from typing import Optional
import fal_client
import asyncio
import os

async def generate_image(prompt: str, model: str = "fal-ai/ideogram/v2", aspect_ratio: str = "1:1", expand_prompt: bool = True, style: str = "auto", negative_prompt: str = "") -> str:
    """
    Generate an image using FAL AI based on a text prompt.
    """
    fal_key = os.getenv("FAL_KEY")
    print(f"FAL_KEY in environment: {fal_key[:4] if fal_key else 'Not set'}...")

    def on_queue_update(update):
        if isinstance(update, fal_client.InProgress):
            for log in update.logs:
                print(log["message"])

    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: fal_client.subscribe(
                model,
                arguments={
                    "prompt": prompt,
                    "aspect_ratio": aspect_ratio,
                    "expand_prompt": expand_prompt,
                    "style": style,
                    "negative_prompt": negative_prompt
                },
                with_logs=True,
                on_queue_update=on_queue_update,
            )
        )
        print(f"Raw FAL response: {result}")
        if result and isinstance(result, dict) and "images" in result and len(result["images"]) > 0:
            return result["images"][0]["url"]
        return "Image generation completed, but no URL returned."
    except Exception as e:
        return f"Error generating image: {str(e)}"