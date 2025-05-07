# Generic Utility functions for the project
# may be even removed
import os
import cv2
import matplotlib.pyplot as plt


def load_image(path):
    """Load an image from the specified path"""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Image file not found: {path}")

    image = cv2.imread(path)
    if image is None:
        raise IOError(f"Could not open or read image: {path}")

    return image


def save_image(image, path):
    """Save an image to the specified path"""
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    return cv2.imwrite(path, image)


def display_comparison(original, filtered, title="Comparison"):
    """Display a side-by-side comparison of original and filtered images"""
    # Convert from BGR to RGB for display
    orig_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    filtered_rgb = cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB)

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(orig_rgb)
    plt.title("Original Image")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(filtered_rgb)
    plt.title(title)
    plt.axis('off')

    plt.tight_layout()
    plt.show()


def ensure_dir_exists(directory):
    """Make sure the specified directory exists"""
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    return directory