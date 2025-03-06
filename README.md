# MCP Tool Server for Logo Generation

This server provides logo generation capabilities using FAL AI, with tools for image generation, background removal, and automatic scaling.

## Installation

1. Install `uv` (Universal Virtualenv):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows
```

3. Install dependencies:

```bash
uv pip install -r requirements.txt
```

4. Set up your environment variables:
   - Create a `.env` file in the root directory
   - Add your FAL AI API key:

```bash
FAL_KEY=your_fal_ai_key_here
```

## Running the Server

Start the server with:

```bash
python run_server.py
```

The server will be available at `http://127.0.0.1:7777`

## Cursor IDE Configuration

1. Open Cursor Settings
2. Navigate to the MCP section
3. Add the following configuration:
   - URL: `http://127.0.0.1:7777/sse`
   - Connection Type: `SSE`
   - Enable the connection

## Notes

- Always reference `@logo-creation.mdc` in your Cursor Composer for consistent results
- Steps are defined in `@logo-creation.mdc` but tools can be used independently
- All generated logos will be saved in the `downloads` directory
- Each logo is automatically generated in three sizes:
  - Original size
  - 32x32 pixels
  - 128x128 pixels
- All logos maintain transparency in their final PNG format
- Prompts created by agent are informed by examples and prompt structure seen in server.py. You can customize the prompt structure by editing the server.py file.
- You can use the generate_image tool to generate any image you want, not just logos

## Requirements

- Python 3.8+
- FAL AI API key (required for image generation)
- Active internet connection

## References

- [Cursor MCP Documentation](https://docs.cursor.com/context/model-context-protocol)
- [Model Context Protocol Introduction](https://modelcontextprotocol.io/introduction)
- [FAL AI Dashboard](https://fal.ai/dashboard)
