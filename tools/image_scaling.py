from PIL import Image
import os
from typing import List, Tuple

async def scale_image(input_path: str, sizes: List[Tuple[int, int]] = [(32, 32), (128, 128)]) -> str:
    """
    Scale an image to multiple specified sizes while preserving transparency.
    
    Args:
        input_path: Path to the input image
        sizes: List of (width, height) tuples for desired output sizes
    
    Returns:
        str: Message indicating where the scaled images were saved
    """
    try:
        if not os.path.exists(input_path):
            return f"Error: Input file {input_path} does not exist"

        # Open the image while preserving transparency
        with Image.open(input_path) as img:
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Get the base filename and directory
            directory = os.path.dirname(input_path)
            filename = os.path.splitext(os.path.basename(input_path))[0]
            
            scaled_files = []
            # Create scaled versions
            for width, height in sizes:
                # Resize the image using high-quality resampling
                scaled = img.resize((width, height), Image.Resampling.LANCZOS)
                
                # Generate output filename
                output_filename = f"{filename}_{width}x{height}.png"
                output_path = os.path.join(directory, output_filename)
                
                # Save with transparency
                scaled.save(output_path, "PNG")
                scaled_files.append(output_path)
            
            return f"Successfully created scaled versions: {', '.join(scaled_files)}"
            
    except Exception as e:
        return f"Error scaling image: {str(e)}" 