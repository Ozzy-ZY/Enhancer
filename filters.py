import numpy as np
from helpers.brightness_helpers import get_brightness_factor
from helpers.edge_helpers import get_sobel_kernels, apply_convolution, normalize_edges
import cv2
from helpers.unsharp_mask_helpers import gaussian_kernel, convolve2d
from helpers.gaussian_noise_helpers import add_gaussian_noise
from helpers.salt_pepper_noise_helpers import add_salt_pepper_noise
from helpers.channel_swap_helpers import apply_channel_swap

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

def unsharp_mask(image, ksize=(5,5), sigma=1.0, amount=1.0, threshold=0):
    """
    Manual unsharp masking (no OpenCV).

    Parameters:
        image (ndarray): Input H×W or H×W×C uint8 image.
        ksize (tuple): (kernel_height, kernel_width), both odd.
        sigma (float): Gaussian sigma.
        amount (float): Strength of sharpening (>0).
        threshold (int): Minimum difference to sharpen (optional).

    Returns:
        sharpened (ndarray): uint8 sharpened image.
    """
    # 1) Build kernel & blur
    kh, kw = ksize
    kernel = gaussian_kernel(kh, sigma)
    img_float = image.astype(np.float32)
    blurred = convolve2d(img_float, kernel)

    # 2) Mask = original - blurred
    mask = img_float - blurred

    # 3) Optionally zero out small differences
    if threshold > 0:
        low_contrast = np.abs(mask) < threshold
        mask[low_contrast] = 0

    # 4) Add scaled mask back
    sharpened = img_float + amount * mask

    # 5) Clip and convert back
    sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
    return sharpened

def apply_edge_detection(image, sensitivity=1.0, direction='both'):# 0.1 => 2.0
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