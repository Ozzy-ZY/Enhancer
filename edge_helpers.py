import numpy as np
from scipy.signal import convolve2d

def get_sobel_kernels():
    """Return the Sobel kernels for horizontal and vertical edge detection"""
    # Sobel kernels
    sobel_x = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])
    
    sobel_y = np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ])
    
    return sobel_x, sobel_y

def apply_convolution(image, kernel):
    """Apply 2D convolution to the image using the given kernel"""
    # Use scipy's optimized convolution
    return convolve2d(image, kernel, mode='same', boundary='symm')

def normalize_edges(edges, sensitivity=1.0):
    """Normalize edge values to 0-255 range and apply sensitivity adjustment"""
    # Normalize to 0-1 range
    edges = (edges - edges.min()) / (edges.max() - edges.min())
    # Apply sensitivity
    edges = edges * sensitivity
    # Clip to 0-1 range
    edges = np.clip(edges, 0, 1)
    # Convert to uint8
    return (edges * 255).astype(np.uint8) 