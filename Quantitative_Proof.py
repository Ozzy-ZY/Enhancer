

import cv2
import numpy as np

def variance_of_laplacian(image: np.ndarray) -> float:
    """
    Compute the variance of the Laplacian (focus measure).
    A higher value indicates a sharper image.
    """
    # Ensure grayscale
    if image.ndim == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    return float(lap.var())

def sobel_gradient_energy(image: np.ndarray) -> float:
    """
    Sum of Sobel gradient magnitudes across the image.
    """
    if image.ndim == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    # Compute gradients
    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    # Sum of magnitudes
    return float(np.sum(np.sqrt(gx**2 + gy**2)))

