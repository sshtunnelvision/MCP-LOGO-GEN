# tools/image_gen.py
from typing import Optional
import fal_client
import asyncio

async def generate_image(prompt: str, model: str = "fal-ai/recraft-v3") -> str:
    """
    Generate an image using FAL AI based on a text prompt.

    Args:
        prompt: The text description for the image.
        model: The FAL AI model to use (default: recraft-v3).

    Returns:
        URL of the generated image or an error message.
    """
    def on_queue_update(update):
        if isinstance(update, fal_client.InProgress):
            for log in update.logs:
                print(log["message"])

    try:
        # Run synchronous fal_client.subscribe in an executor
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: fal_client.subscribe(
                model,
                arguments={
                    "prompt": prompt,
                    "image_size": "square_hd",  # Adding default image size
                    "style": "realistic_image"   # Adding default style
                },
                with_logs=True,
                on_queue_update=on_queue_update,
            )
        )
        
        # Extract the image URL from the result according to the API response structure
        if "images" in result and len(result["images"]) > 0:
            return result["images"][0]["url"]
        return "Image generation completed, but no image URL in response."
    except Exception as e:
        return f"Error generating image: {str(e)}"