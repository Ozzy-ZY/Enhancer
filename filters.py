import numpy as np
from brightness_helpers import get_brightness_factor, get_brightness_description
from edge_helpers import get_sobel_kernels, apply_convolution, normalize_edges

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

def apply_edge_detection(image, sensitivity=1.0, direction='both'):
    """
    Apply Sobel edge detection to the image
    
    Args:
        image: Input image (will be converted to grayscale if color)
        sensitivity: Edge detection sensitivity (default: 1.0)
        direction: Edge detection direction ('horizontal', 'vertical', or 'both')
    
    Returns:
        Edge detected image
    """
    # Convert to grayscale if color image
    if len(image.shape) == 3:
        image = apply_grayscale(image)[..., 0]  # Take one channel since it's grayscale
    
    # Get Sobel kernels
    sobel_x, sobel_y = get_sobel_kernels()
    
    # Apply edge detection based on direction
    if direction == 'horizontal':
        edges = apply_convolution(image, sobel_x)
    elif direction == 'vertical':
        edges = apply_convolution(image, sobel_y)
    else:  # both
        edges_x = apply_convolution(image, sobel_x)
        edges_y = apply_convolution(image, sobel_y)
        # Calculate magnitude of gradient
        edges = np.sqrt(edges_x**2 + edges_y**2)
    
    # Normalize and apply sensitivity
    edges = normalize_edges(edges, sensitivity)
    
    # Convert back to 3-channel image
    return np.stack([edges, edges, edges], axis=-1)