import cv2

def remove_noise(image, method="median", **kwargs):
    """
    Remove noise from the image using the specified method.
    Available methods: 'median', 'gaussian', 'bilateral'
    """
    if method == "median":
        ksize = kwargs.get("ksize", 5)
        return cv2.medianBlur(image, ksize)
    
    elif method == "gaussian":
        ksize = kwargs.get("ksize", (5, 5))
        sigma = kwargs.get("sigma", 0)
        return cv2.GaussianBlur(image, ksize, sigma)
    
    elif method == "bilateral":
        d = kwargs.get("d", 9)
        sigma_color = kwargs.get("sigma_color", 75)
        sigma_space = kwargs.get("sigma_space", 75)
        return cv2.bilateralFilter(image,d,sigma_color,sigma_space)
    
    else:
        raise ValueError(f"Unknown noise removal method: {method}")
