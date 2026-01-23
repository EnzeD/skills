#!/usr/bin/env python3
"""
Difference matting for true alpha channel extraction.

This technique generates an image on both white and black backgrounds,
then mathematically extracts the true alpha channel from the difference.

Usage:
    from transparency import extract_alpha_difference_matting

    final = extract_alpha_difference_matting(img_on_white, img_on_black)
    final.save("output.png")  # RGBA with true transparency
"""

import math
import numpy as np
from PIL import Image


def extract_alpha_difference_matting(
    img_on_white: Image.Image,
    img_on_black: Image.Image
) -> Image.Image:
    """
    Extract true alpha channel using difference matting technique.

    Algorithm:
    - If a pixel is 100% opaque, it looks the same on black and white (distance = 0)
    - If a pixel is 100% transparent, it shows the background (distance = max)
    - Semi-transparent pixels fall in between

    Args:
        img_on_white: Image generated with pure white (#FFFFFF) background
        img_on_black: Same image with pure black (#000000) background

    Returns:
        RGBA image with true transparency extracted
    """
    # Convert to numpy arrays
    white_arr = np.array(img_on_white.convert('RGB'), dtype=np.float32)
    black_arr = np.array(img_on_black.convert('RGB'), dtype=np.float32)

    # Distance between pure white (255,255,255) and pure black (0,0,0)
    # sqrt(255^2 + 255^2 + 255^2) ≈ 441.67
    bg_dist = math.sqrt(3 * 255 * 255)

    # Calculate pixel distance between the two images
    diff = white_arr - black_arr
    pixel_dist = np.sqrt(np.sum(diff ** 2, axis=2))

    # Calculate alpha: opaque pixels have small distance, transparent have large
    alpha = 1.0 - (pixel_dist / bg_dist)
    alpha = np.clip(alpha, 0, 1)

    # Recover original color from the black background version
    # C_observed = C_original * alpha + background * (1 - alpha)
    # For black background: C_observed = C_original * alpha
    # So: C_original = C_observed / alpha
    alpha_expanded = np.expand_dims(alpha, axis=2)
    alpha_safe = np.where(alpha_expanded > 0.01, alpha_expanded, 1.0)

    rgb_recovered = black_arr / alpha_safe
    rgb_recovered = np.clip(rgb_recovered, 0, 255).astype(np.uint8)

    # Combine RGB with alpha channel
    alpha_uint8 = (alpha * 255).astype(np.uint8)

    # Create RGBA image
    rgba = np.dstack((rgb_recovered, alpha_uint8))

    return Image.fromarray(rgba, 'RGBA')


def background_is_black(image: Image.Image, threshold: int = 20) -> bool:
    """
    Verify that an image has a black background by checking corner pixels.

    Args:
        image: Image to check
        threshold: Maximum average RGB value for "black" (default 20)

    Returns:
        True if all corners are near-black
    """
    rgb = image.convert("RGB")
    w, h = rgb.size
    corners = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    for x, y in corners:
        r, g, b = rgb.getpixel((x, y))
        if (r + g + b) / 3 > threshold:
            return False
    return True


def generate_transparent_image(
    client,
    prompt: str,
    aspect_ratio: str = "1:1",
    image_size: str = "2K",
    model: str = "gemini-3-pro-image-preview",
    max_black_attempts: int = 5
) -> Image.Image:
    """
    Generate an image with true transparency using difference matting.

    This is a complete workflow that:
    1. Generates on white background
    2. Edits to black background
    3. Extracts alpha via difference matting

    Args:
        client: google.genai.Client instance
        prompt: Image generation prompt (will be augmented with background instruction)
        aspect_ratio: Output aspect ratio
        image_size: Output resolution (1K, 2K, 4K)
        model: Model to use
        max_black_attempts: Max retries for black background conversion

    Returns:
        RGBA image with true transparency
    """
    from google.genai import types
    import io
    import time

    # Step 1: Generate on white background
    white_prompt = f"{prompt}\n\nIMPORTANT: Use a pure white background (#FFFFFF, RGB 255,255,255). Do not use white anywhere on the subject itself."

    response = client.models.generate_content(
        model=model,
        contents=white_prompt,
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=image_size
            ),
        ),
    )

    img_on_white = None
    for part in response.parts:
        if part.inline_data is not None:
            img_on_white = Image.open(io.BytesIO(part.inline_data.data))
            break

    if img_on_white is None:
        raise RuntimeError("Failed to generate image on white background")

    # Step 2: Edit to black background
    img_on_black = None
    for attempt in range(1, max_black_attempts + 1):
        black_prompt = """Replace ONLY the background with pure black (#000000, RGB 0,0,0).

Keep EVERYTHING else exactly unchanged:
- Same subject in exact same position
- Same colors on the subject
- Same details and features

Only change the white background pixels to pure black."""

        response = client.models.generate_content(
            model=model,
            contents=[img_on_white, black_prompt],
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                    image_size=image_size
                ),
            ),
        )

        for part in response.parts:
            if part.inline_data is not None:
                img_on_black = Image.open(io.BytesIO(part.inline_data.data))
                break

        if img_on_black is not None and background_is_black(img_on_black):
            break

        if attempt < max_black_attempts:
            time.sleep(1)

    if img_on_black is None or not background_is_black(img_on_black):
        raise RuntimeError("Failed to convert to black background after retries")

    # Step 3: Extract alpha
    return extract_alpha_difference_matting(img_on_white, img_on_black)
