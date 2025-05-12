import numpy as np
from brightness_helpers import get_brightness_factor
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

def gaussian_kernel(ksize=5, sigma=1.0):
    """
    Create a 2D Gaussian kernel by outer-product of two 1D Gaussians.
    ksize: odd integer > 1, kernel width & height
    sigma: standard deviation of the Gaussian
    """
    # 1D coordinates centered at zero
    ax = np.linspace(-(ksize // 2), ksize // 2, ksize)
    gauss1d = np.exp(-0.5 * (ax / sigma)**2)
    gauss1d /= gauss1d.sum()              # normalize
    # Outer product to get 2D kernel
    kernel = np.outer(gauss1d, gauss1d)
    return kernel


def convolve2d(image, kernel):
    """
    Convolve a 2D (H×W) or 3D (H×W×C) image with a 2D kernel.
    Pads edges with reflect mode.
    """
    if image.ndim == 2:
        image = image[:, :, None]   # make H×W×1 for uniformity

    h, w, channels = image.shape
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2

    # Pad each channel
    padded = np.pad(image,
                    ((pad_h, pad_h), (pad_w, pad_w), (0, 0)),
                    mode='reflect')

    # Prepare output
    out = np.zeros_like(image, dtype=np.float32)

    # Slide kernel
    for y in range(h):
        for x in range(w):
            for c in range(channels):
                region = padded[y:y+kh, x:x+kw, c]
                out[y, x, c] = np.sum(region * kernel)

    return out.squeeze()

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