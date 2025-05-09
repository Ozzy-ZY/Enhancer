def get_brightness_factor(level):
    """Get the brightness factor for a given level"""
    levels = {
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
    if level not in levels:
        raise ValueError(f"Brightness level must be between -4 and 4, got {level}")
    return levels[level]

def get_brightness_description(level):
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