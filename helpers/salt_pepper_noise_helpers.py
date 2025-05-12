import numpy as np

def add_salt_pepper_noise(image, intensity=0.1):
    """
    Add salt and pepper noise to an image
    
    Args:
        image: Input image (numpy array)
        intensity: Noise intensity, controls the amount of noise (default: 0.1)
    
    Returns:
        Image with added salt and pepper noise
    """
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