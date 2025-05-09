import numpy as np
from brightness_helpers import get_brightness_factor, get_brightness_description

def apply_brightness(image, level=0):
    """Apply brightness adjustment with specified level"""
    factor = get_brightness_factor(level)
    return np.clip(image * factor, 0, 255).astype(np.uint8)

def apply_all_brightness_levels(image):
    """Apply all brightness levels and return a dictionary of results"""
    results = {}
    for level in range(-4, 5):
        if level == 0:  # Skip original image
            continue
        results[level] = apply_brightness(image, level)
    return results

def apply_grayscale(image):
    """Convert an image to grayscale using perceptual weights"""
    weights = np.array([0.299, 0.587, 0.114])
    grayscale = np.dot(image[..., :3], weights)
    return np.stack([grayscale, grayscale, grayscale], axis=-1).astype(np.uint8)