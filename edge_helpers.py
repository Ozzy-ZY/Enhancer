import numpy as np
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
    """Original slow implementation of convolution"""
    # Get image dimensions
    height, width = image.shape[:2]
    kernel_size = kernel.shape[0]
    pad_size = kernel_size // 2
    # Pad the image
    padded = np.pad(image, pad_size, mode='symmetric')
    # Initialize output
    output = np.zeros_like(image, dtype=np.float32)
    # Apply convolution
    for i in range(height):
        for j in range(width):
            # Extract the region of interest
            region = padded[i:i+kernel_size, j:j+kernel_size]
            # Apply the kernel
            output[i, j] = np.sum(region * kernel)
    
    return output

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