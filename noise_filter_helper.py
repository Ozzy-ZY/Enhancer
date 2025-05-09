import numpy as np
from scipy import ndimage

def smooth_image_with_gaussian_blur(image, sigma=1.0):
    # For color images, apply filter to each channel
    if len(image.shape) > 2:
        result = np.zeros_like(image)
        for i in range(image.shape[2]):
            result[:, :, i] = ndimage.gaussian_filter(image[:, :, i], sigma=sigma)
    else:
        result = ndimage.gaussian_filter(image, sigma=sigma)

    return result.astype(np.uint8)


def remove_noise_with_median_filter(image, kernel_size=3):
    # For color images, apply filter to each channel
    if len(image.shape) > 2:
        result = np.zeros_like(image)
        for i in range(image.shape[2]):
            result[:, :, i] = ndimage.median_filter(image[:, :, i], size=kernel_size)
    else:
        result = ndimage.median_filter(image, size=kernel_size)

    return result.astype(np.uint8)