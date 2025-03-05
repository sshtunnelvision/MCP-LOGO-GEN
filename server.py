# server.py
import asyncio
import click
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from tools.image_gen import generate_image
from typing import Optional
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from mcp.server.sse import SseServerTransport
from starlette.routing import Mount, Route
import signal
import uvicorn

# Debug: Print current working directory
print(f"Current working directory: {os.getcwd()}")

# Load environment variables
print("Loading environment variables...")
load_dotenv(verbose=True)
print(f"Environment after load_dotenv: FAL_KEY={'*' * len(os.getenv('FAL_KEY')) if os.getenv('FAL_KEY') else 'Not found'}")

# Initialize the server
app = FastAPI(debug=True)
server = Server("image-gen-server")
sse = SseServerTransport("/messages/")

# Add shutdown event handler
@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down server gracefully...")
    # Add any cleanup tasks here if needed
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)
    print("Server shutdown complete")

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """List available resources."""
    return []

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read a specific resource."""
    raise ValueError(f"Unsupported resource: {uri}")

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """List available prompts."""
    return []

@server.get_prompt()
async def handle_get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
    """Get a specific prompt."""
    raise ValueError(f"Unknown prompt: {name}")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="generate_image",
            description="Generate an image from a text prompt using FAL AI",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Text prompt to generate the image"
                    },
                    "model": {
                        "type": "string",
                        "description": "Model to use for generation",
                        "default": "fal-ai/recraft-v3"
                    }
                },
                "required": ["prompt"]
            }
        )
    ]

class ImageGenToolHandler:
    async def handle(self, name: str, arguments: dict | None) -> list[types.TextContent | types.ImageContent]:
        print(f"Generating image with prompt: {arguments.get('prompt')}")
        result = await generate_image(
            arguments.get("prompt"),
            arguments.get("model", "fal-ai/recraft-v3")
        )
        print(f"Image generation result: {result}")
        if result.startswith("http"):
            return [types.TextContent(type="text", text=f"Generated image URL: {result}")]
        return [types.TextContent(type="text", text=result)]

tool_handlers = {
    "generate_image": ImageGenToolHandler()
}

@server.call_tool()
async def handle_call_tool(
    name: str,
    arguments: dict | None
) -> list[types.TextContent | types.ImageContent]:
    """Handle tool execution requests."""
    if name in tool_handlers:
        return await tool_handlers[name].handle(name, arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def handle_sse(request):
    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await server.run(
            streams[0],
            streams[1],
            InitializationOptions(
                server_name="image-gen-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

@click.command()
@click.option("--port", default=7777, help="Port to listen on")
def main(port: int) -> int:
    # Ensure FAL_KEY is set
    fal_key = os.getenv("FAL_KEY")
    if not fal_key:
        print("Warning: FAL_KEY environment variable not found, checking FAL_API_KEY...")
        fal_key = os.getenv("FAL_API_KEY")
        if not fal_key:
            print("Error: Neither FAL_KEY nor FAL_API_KEY environment variables are set")
            exit(1)
        os.environ["FAL_KEY"] = fal_key

    print("Starting image generation server...")

    # Add routes
    app.add_route("/sse", handle_sse)
    app.mount("/messages", sse.handle_post_message)

    # Cool ASCII art log
    print("""
    ===========================================
          🚀 MCP Server is LIVE! 🚀
    ------------------------------------------- 
    |  Status: Running                        |
    |  Transport: SSE                         |
    |  URL: http://127.0.0.1:{}              |
    |  Ready for Cursor MCP client            |
    |  Auto-reload: Enabled                   |
    ------------------------------------------- 
    Listening for requests... 🎉
    ===========================================
    """.format(port))

    config = uvicorn.Config(
        app=app,
        host="127.0.0.1",
        port=port,
        reload=True,  # Enable auto-reload
        reload_dirs=["mcp_tool_server"],  # Watch this directory for changes
        workers=1
    )
    server = uvicorn.Server(config)
    server.run()
    return 0

if __name__ == "__main__":
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, lambda sig, frame: os._exit(0))
    signal.signal(signal.SIGTERM, lambda sig, frame: os._exit(0))
    main()