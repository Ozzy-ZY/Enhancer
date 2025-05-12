import numpy as np

def add_gaussian_noise(image, intensity=0.1):
    """
    Add Gaussian noise to an image
    
    Args:
        image: Input image (numpy array)
        intensity: Noise intensity, controls standard deviation (default: 0.1)
    
    Returns:
        Image with added Gaussian noise
    """
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