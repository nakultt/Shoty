"""Utility functions for the PixelPipe agent."""

import base64
import os


def encode_image(image_path: str) -> str:
    """Encodes a local image to Base64 for the Ollama API.
    
    Args:
        image_path: Path to the image file.
        
    Returns:
        Base64 encoded string of the image.
        
    Raises:
        FileNotFoundError: If the image file doesn't exist.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"❌ Image not found at {image_path}")
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
