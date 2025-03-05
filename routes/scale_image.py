from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Tuple
from ..tools import scale_image

router = APIRouter()

class ScaleImageRequest(BaseModel):
    input_path: str
    sizes: List[Tuple[int, int]] = [(32, 32), (128, 128)]

@router.post("/scale-image")
async def scale_image_route(request: ScaleImageRequest):
    """
    Scale an image to specified sizes while preserving transparency.
    """
    try:
        result = await scale_image(request.input_path, request.sizes)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 