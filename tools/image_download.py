from typing import Optional
import aiohttp
import asyncio
import os
from urllib.parse import urlparse
import mimetypes

async def download_image_from_url(image_url: str, output_dir: str = "downloads") -> str:
    """
    Download an image from a URL and save it locally.
    """
    try:
        # Create downloads directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Extract filename from URL or generate one
        parsed_url = urlparse(image_url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            # If no filename in URL, create one based on timestamp
            content_type = mimetypes.guess_type(image_url)[0]
            ext = mimetypes.guess_extension(content_type) if content_type else '.jpg'
            filename = f"image_{int(asyncio.get_event_loop().time())}{ext}"

        output_path = os.path.join(output_dir, filename)

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status != 200:
                    return f"Error downloading image: HTTP {response.status}"
                
                # Verify it's an image from content-type
                content_type = response.headers.get('content-type', '')
                if not content_type.startswith('image/'):
                    return f"Error: URL does not point to an image (content-type: {content_type})"

                # Download and save the image
                with open(output_path, 'wb') as f:
                    while True:
                        chunk = await response.content.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)

        return f"Image successfully downloaded to: {output_path}"
    except Exception as e:
        return f"Error downloading image: {str(e)}" 