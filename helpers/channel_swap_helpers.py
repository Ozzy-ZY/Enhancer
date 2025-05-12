import numpy as np
import cv2

def apply_channel_swap(image, mode='rgb'):
    """
    Swap or manipulate color channels of an image
    
    Args:
        image: Input image (numpy array)
        mode: Channel manipulation mode:
            'rgb' - Original (no change)
            'rbg' - Swap red and blue
            'grb' - Swap green and red
            'gbr' - Green to blue, blue to red, red to green
            'brg' - Blue to red, red to green, green to blue
            'bgr' - Reverse order (OpenCV default)
            'r' - Keep only red channel
            'g' - Keep only green channel
            'b' - Keep only blue channel
    
    Returns:
        Image with modified color channels (numpy array)
    """
    if mode == 'rgb':
        return image.copy()
    
    # Split channels
    b, g, r = cv2.split(image)
    
    # Apply different channel combinations
    if mode == 'rbg':
        return cv2.merge((g, b, r))
    elif mode == 'grb':
        return cv2.merge((b, r, g))
    elif mode == 'gbr':
        return cv2.merge((g, r, b))
    elif mode == 'brg':
        return cv2.merge((r, b, g))
    elif mode == 'bgr':
        return cv2.merge((r, g, b))
    elif mode == 'r':
        return cv2.merge(( np.zeros_like(r), np.zeros_like(r), r))
    elif mode == 'g':
        return cv2.merge((np.zeros_like(g), g, np.zeros_like(g)))
    elif mode == 'b':
        return cv2.merge((b, np.zeros_like(b), np.zeros_like(b)))
    else:
        raise ValueError(f"Unknown channel mode: {mode}")