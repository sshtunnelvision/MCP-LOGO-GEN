# server.py
import asyncio
from mcp.server.fastmcp import FastMCP
from tools.image_gen import generate_image
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Initialize the FastMCP server (still used for tool registration)
print("Starting server setup...")
mcp = FastMCP("MultiToolServer")
print("Server initialized.")

# Register the image generation tool with MCP
@mcp.tool()
async def generate_image_tool(prompt: str, model: Optional[str] = "fal-ai/recraft-v3") -> str:
    """Generate an image from a text prompt using FAL AI.

    Args:
        prompt: The text description for the image.
        model: The FAL AI model to use (optional, defaults to recraft-v3).

    Returns:
        URL of the generated image or an error message.
    """
    print(f"Generating image with prompt: {prompt}")
    result = await generate_image(prompt, model)
    print(f"Image generation result: {result}")
    return result

# Pydantic model for request body
class GenerateImageRequest(BaseModel):
    prompt: str
    model: Optional[str] = "fal-ai/recraft-v3"

# FastAPI app
app = FastAPI(
    title="MultiToolServer API",
    description="A server for managing multiple tools via HTTP",
    version="1.0.0"
)

# HTTP endpoint for the image generation tool
@app.post("/tools/generate_image", response_model=dict)
async def http_generate_image(request: GenerateImageRequest):
    """Generate an image from a text prompt using FAL AI.

    Args:
        request: JSON body containing prompt and optional model.

    Returns:
        dict: {"result": "<image_url_or_error_message>"}
    """
    try:
        result = await generate_image_tool(request.prompt, request.model)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Cool ASCII art log
def print_server_running():
    message = """
    ===========================================
          🚀 MCP Tool Server is LIVE! 🚀
    ------------------------------------------- 
    |  Status: Running                        |
    |  Transport: HTTP                        |
    |  Endpoint: http://localhost:8000        |
    ------------------------------------------- 
    Listening for requests... 🎉
    ===========================================
    """
    print(message)

# Run the server with FastAPI
if __name__ == "__main__":
    print("Running server...")
    print_server_running()
    uvicorn.run(app, host="0.0.0.0", port=8000)