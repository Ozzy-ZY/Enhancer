import numpy as np

def gaussian_kernel(ksize=5, sigma=1.0):
    """
    Create a 2D Gaussian kernel by outer-product of two 1D Gaussians.
    ksize: odd integer > 1, kernel width & height
    sigma: standard deviation of the Gaussian
    """
    # 1D coordinates centered at zero
    ax = np.linspace(-(ksize // 2), ksize // 2, ksize)
    gauss1d = np.exp(-0.5 * (ax / sigma)**2)
    gauss1d /= gauss1d.sum()              # normalize
    # Outer product to get 2D kernel
    kernel = np.outer(gauss1d, gauss1d)
    return kernel


def convolve2d(image, kernel):
    """
    Convolve a 2D (H×W) or 3D (H×W×C) image with a 2D kernel.
    Pads edges with reflect mode.
    """
    if image.ndim == 2:
        image = image[:, :, None]   # make H×W×1 for uniformity

    h, w, channels = image.shape
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2

    # Pad each channel
    padded = np.pad(image,
                    ((pad_h, pad_h), (pad_w, pad_w), (0, 0)),
                    mode='reflect')

    # Prepare output
    out = np.zeros_like(image, dtype=np.float32)

    # Slide kernel
    for y in range(h):
        for x in range(w):
            for c in range(channels):
                region = padded[y:y+kh, x:x+kw, c]
                out[y, x, c] = np.sum(region * kernel)

    return out.squeeze()