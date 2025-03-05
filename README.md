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

## Cursor IDE Configuration

1. Open Cursor Settings
2. Navigate to the MCP section
3. Add the following configuration:
   - URL: `http://127.0.0.1:7777/sse`
   - Connection Type: `SSE`
   - Enable the connection

## Logo Generation Examples

Here are 10 diverse examples of logos you can create:

1. **Minimalist Nature Logo**

```
"Simple pine tree logo, minimal geometric design, centered, white background"
```

2. **Tech Company Wordmark**

```
"TECH, modern sans-serif wordmark, bold letters, centered white background"
```

3. **Abstract Symbol**

```
"Abstract geometric shape logo, interconnected lines forming a dynamic symbol, centered white background"
```

4. **Mascot Logo**

```
"Friendly owl mascot logo, simple cartoon style, centered white background"
```

5. **Monogram/Letter Logo**

```
"Letter M logo, elegant typography with creative negative space, centered white background"
```

6. **Vintage Badge**

```
"Circular vintage badge logo, clean lines, centered white background"
```

7. **Food/Restaurant Logo**

```
"Fork and knife crossed icon, culinary logo design, centered white background"
```

8. **Medical/Healthcare Symbol**

```
"Medical cross with heart symbol, professional healthcare logo, centered white background"
```

9. **Educational/Academic Logo**

```
"Open book with graduation cap logo, academic symbol, centered white background"
```

10. **Music/Entertainment Logo**

```
"Musical note with dynamic wave design, entertainment logo, centered white background"
```

## Notes

- Always reference `@logo-creation.mdc` in your Cursor Composer for consistent results
- All generated logos will be saved in the `downloads` directory
- Each logo is automatically generated in three sizes:
  - Original size
  - 32x32 pixels
  - 128x128 pixels
- All logos maintain transparency in their final PNG format
- For best results, always specify "centered", "white background" "2D design" in your prompts
- You can use the generate_image tool to generate any image you want, not just logos

## Requirements

- Python 3.8+
- FAL AI API key (required for image generation)
- Active internet connection

## References

- [Cursor MCP Documentation](https://docs.cursor.com/context/model-context-protocol)
- [Model Context Protocol Introduction](https://modelcontextprotocol.io/introduction)
- [FAL AI Dashboard](https://fal.ai/dashboard)
