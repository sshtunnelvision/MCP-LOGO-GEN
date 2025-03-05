import base64
from typing import Optional
import fal_client
import asyncio
import os
from .image_download import download_image_from_url

def is_base64(s: str) -> bool:
    """Check if a string is base64 encoded."""
    try:
        # Check if string starts with data URI scheme
        if s.startswith('data:image'):
            # Extract the base64 part after the comma
            base64_str = s.split(',')[1]
            # Try to decode it
            base64.b64decode(base64_str)
            return True
    except Exception:
        pass
    return False

async def remove_background(
    image_url: str,
    sync_mode: bool = True,
    crop_to_bbox: bool = False
) -> str:
    """
    Remove background from an image using FAL AI.
    """
    fal_key = os.getenv("FAL_KEY")
    print(f"FAL_KEY in environment: {fal_key[:4] if fal_key else 'Not set'}...")

    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: fal_client.subscribe(
                "fal-ai/bria/background/remove",
                arguments={
                    "image_url": image_url,
                    "sync_mode": sync_mode
                }
            )
        )
        
        # Handle the response according to the new schema
        if isinstance(result, dict) and "image" in result:
            image_data = result["image"]
            if "url" in image_data:
                print("Successfully removed background from image")
                return image_data["url"]  # Return the FAL-hosted URL directly
            else:
                return "Background removal completed, but no image URL was returned"
        else:
            return f"Unexpected response format: {str(result)}"
    except Exception as e:
        return f"Error removing background: {str(e)}" 