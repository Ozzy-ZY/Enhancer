import cv2

def apply_invert(image):
    """
    Invert the colors of the image.
    Creates a negative version of the original image.
    """
    # inverts each pixel value: 255 - value.
    return cv2.bitwise_not(image)