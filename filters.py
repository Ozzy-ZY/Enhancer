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


def add_gaussian_noise(image, intensity=0.1):
    # Convert to float for calculations
    img_float = image.astype(np.float32)

    # Generate Gaussian noise
    std_dev = intensity * 255.0
    noise = np.random.normal(loc=0, scale=std_dev, size=img_float.shape)

    # Add noise to image
    noisy_img = img_float + noise

    # Clip values to valid range and convert back to uint8
    noisy_img = np.clip(noisy_img, 0, 255).astype(np.uint8)

    return noisy_img


def add_salt_pepper_noise(image, intensity=0.1):
    # Create a copy of the image
    noisy_image = np.copy(image)

    # Generate salt noise (white pixels)
    salt_mask = np.random.random(size=image.shape[:2]) < (intensity / 2)

    # Generate pepper noise (black pixels)
    pepper_mask = np.random.random(size=image.shape[:2]) < (intensity / 2)

    # Apply salt noise to all channels
    if len(image.shape) > 2:  # Color image
        for i in range(image.shape[2]):
            noisy_image[salt_mask, i] = 255
            noisy_image[pepper_mask, i] = 0
    else:  # Grayscale image
        noisy_image[salt_mask] = 255
        noisy_image[pepper_mask] = 0

    return noisy_image