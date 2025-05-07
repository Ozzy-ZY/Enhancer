import numpy as np


class ImageFilter:
    """Base class for image filters"""

    def __init__(self, name):
        self.name = name

    def apply(self, image):
        """Apply filter to image"""
        raise NotImplementedError("Subclasses must implement this method")

    def get_name(self):
        return self.name


class BrightnessFilter(ImageFilter):
    """Filter to adjust image brightness"""

    def __init__(self):
        super().__init__("Brightness")
        self.levels = {
            -4: 0.2,
            -3: 0.3,
            -2: 0.5,
            -1: 0.7,
            0: 1.0,
            1: 1.3,
            2: 1.6,
            3: 1.9,
            4: 2.2
        }

    def apply(self, image, level=0):
        """Apply brightness adjustment with specified level"""
        if level not in self.levels:
            raise ValueError(f"Brightness level must be between -4 and 4, got {level}")

        factor = self.levels[level]
        return np.clip(image * factor, 0, 255).astype(np.uint8)

    def apply_all_levels(self, image):
        """Apply all brightness levels and return a dictionary of results"""
        results = {}
        for level, factor in self.levels.items():
            if level == 0:  # Skip original image
                continue
            results[level] = self.apply(image, level)
        return results

    def get_level_description(self, level):
        """Get a description for a specific brightness level"""
        descriptions = {
            -4: "Very dark (20% brightness)",
            -3: "Darker (30% brightness)",
            -2: "Somewhat dark (50% brightness)",
            -1: "Slightly dark (70% brightness)",
            0: "Normal (100% brightness)",
            1: "Slightly bright (130% brightness)",
            2: "Somewhat bright (160% brightness)",
            3: "Brighter (190% brightness)",
            4: "Very bright (220% brightness)"
        }
        return descriptions.get(level, "Unknown level")


# Add more filter classes here as you develop them
class GrayscaleFilter(ImageFilter):
    """Filter to convert an image to grayscale"""

    def __init__(self):
        super().__init__("Grayscale")

    def apply(self, image, _=None):
        # Using weighted channels for perceptual grayscale
        weights = np.array([0.299, 0.587, 0.114])
        grayscale = np.dot(image[..., :3], weights)
        return np.stack([grayscale, grayscale, grayscale], axis=-1).astype(np.uint8)

# More filters can be added here...