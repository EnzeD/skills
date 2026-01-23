#!/usr/bin/env python3
"""
CLI for generating images with Google Gemini.

Usage:
    python scripts/generate.py "a cute banana sticker" --output sticker.png
    python scripts/generate.py "pixel art sword" --output sword.png --transparent
    python scripts/generate.py "game logo" --output logo.png --size 4K --ratio 16:9
"""

import argparse
import io
import os
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Google Gemini",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/generate.py "a banana sticker" -o banana.png
  python scripts/generate.py "pixel art sword" -o sword.png --transparent
  python scripts/generate.py "game logo" -o logo.png --size 4K --ratio 16:9
        """
    )
    parser.add_argument("prompt", help="Image generation prompt")
    parser.add_argument("-o", "--output", default="output.png", help="Output filename (default: output.png)")
    parser.add_argument("--transparent", action="store_true", help="Extract transparency using difference matting")
    parser.add_argument("--size", choices=["1K", "2K", "4K"], default="2K", help="Image size (default: 2K)")
    parser.add_argument("--ratio", default="1:1",
                       choices=["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"],
                       help="Aspect ratio (default: 1:1)")
    parser.add_argument("--model", default="gemini-3-pro-image-preview", help="Model to use")

    args = parser.parse_args()

    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass  # dotenv is optional, user may have exported the key directly

    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: No API key found.", file=sys.stderr)
        print("Set GOOGLE_API_KEY in .env or export it directly.", file=sys.stderr)
        print("Get a key at: https://aistudio.google.com/apikey", file=sys.stderr)
        sys.exit(1)

    # Import dependencies
    try:
        from google import genai
        from google.genai import types
        from PIL import Image
    except ImportError as e:
        print(f"Error: Missing dependency - {e}", file=sys.stderr)
        print("Install with: pip install google-genai Pillow numpy", file=sys.stderr)
        sys.exit(1)

    # Initialize client
    client = genai.Client(api_key=api_key)

    if args.transparent:
        # Use transparency workflow
        try:
            import numpy as np
            from transparency import extract_alpha_difference_matting, background_is_black
        except ImportError:
            # Try relative import for when run from repo root
            script_dir = Path(__file__).parent
            sys.path.insert(0, str(script_dir))
            from transparency import extract_alpha_difference_matting, background_is_black

        print(f"Generating transparent image: {args.prompt}")
        print("Step 1/3: Generating on white background...")

        white_prompt = f"{args.prompt}\n\nIMPORTANT: Use a pure white background (#FFFFFF, RGB 255,255,255). Do not use white anywhere on the subject itself."

        response = client.models.generate_content(
            model=args.model,
            contents=white_prompt,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=args.ratio,
                    image_size=args.size
                ),
            ),
        )

        img_on_white = None
        for part in response.parts:
            if part.inline_data is not None:
                img_on_white = Image.open(io.BytesIO(part.inline_data.data))
                break

        if img_on_white is None:
            print("Error: Failed to generate image on white background", file=sys.stderr)
            sys.exit(1)

        print("Step 2/3: Converting to black background...")

        img_on_black = None
        for attempt in range(1, 6):
            black_prompt = """Replace ONLY the background with pure black (#000000, RGB 0,0,0).

Keep EVERYTHING else exactly unchanged:
- Same subject in exact same position
- Same colors on the subject
- Same details and features

Only change the white background pixels to pure black."""

            response = client.models.generate_content(
                model=args.model,
                contents=[img_on_white, black_prompt],
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE'],
                    image_config=types.ImageConfig(
                        aspect_ratio=args.ratio,
                        image_size=args.size
                    ),
                ),
            )

            for part in response.parts:
                if part.inline_data is not None:
                    img_on_black = Image.open(io.BytesIO(part.inline_data.data))
                    break

            if img_on_black is not None and background_is_black(img_on_black):
                break

            print(f"  Retry {attempt}/5 - background not black enough...")

        if img_on_black is None or not background_is_black(img_on_black):
            print("Error: Failed to convert to black background", file=sys.stderr)
            sys.exit(1)

        print("Step 3/3: Extracting transparency...")
        final_image = extract_alpha_difference_matting(img_on_white, img_on_black)

    else:
        # Simple generation
        print(f"Generating image: {args.prompt}")

        response = client.models.generate_content(
            model=args.model,
            contents=args.prompt,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=args.ratio,
                    image_size=args.size
                ),
            ),
        )

        final_image = None
        for part in response.parts:
            if part.inline_data is not None:
                final_image = Image.open(io.BytesIO(part.inline_data.data))
                break

        if final_image is None:
            print("Error: Failed to generate image", file=sys.stderr)
            sys.exit(1)

    # Save output
    final_image.save(args.output)
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
