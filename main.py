# ToDo: add an Interactive-CLI to be facing the user

import os
import time
from filters import apply_brightness, apply_all_brightness_levels, apply_grayscale
from brightness_helpers import get_brightness_description
import utils

def load_image():
    """Prompt user for image path and load it"""
    while True:
        try:
            path = input("Path to input image\n(example: images/delft.jpg) : ").strip()
            current_image = utils.load_image(path)
            print(f"Image loaded successfully: {path}")
            return current_image, path
        except (FileNotFoundError, IOError) as e:
            print(f"Error: {e}")
            retry = input("Try again? (y/n): ").strip().lower()
            if retry != 'y':
                return None, None

def apply_brightness_filter(current_image, output_dir):
    """Apply brightness filter with user-specified level"""
    try:
        level = int(input("Enter brightness level (-4 to 4): "))
        if level < -4 or level > 4:
            print("Invalid level. Must be between -4 and 4.")
            return

        result = apply_brightness(current_image, level)

        # Save the result
        filename = f"brightness_{level:+d}.jpg"
        output_path = os.path.join(output_dir, filename)
        utils.save_image(result, output_path)
        print(f"Saved to {output_path}")

        # Display comparison
        title = f"Brightness level {level:+d} ({get_brightness_description(level)})"
        utils.display_comparison(current_image, result, title)

    except ValueError:
        print("Please enter a number between -4 and 4.")

def save_all_brightness_levels(current_image, output_dir):
    """Save all brightness adjustment levels"""
    results = apply_all_brightness_levels(current_image)

    for level, image in results.items():
        filename = f"brightness_{level:+d}.jpg"
        output_path = os.path.join(output_dir, filename)
        utils.save_image(image, output_path)

    print(f"All brightness levels saved to {output_dir}/")

def apply_grayscale_filter(current_image, output_dir):
    """Apply grayscale filter"""
    result = apply_grayscale(current_image)

    # Save the result
    output_path = os.path.join(output_dir, "grayscale.jpg")
    utils.save_image(result, output_path)
    print(f"Saved to {output_path}")

    # Display comparison
    utils.display_comparison(current_image, result, "Grayscale")

def show_main_menu():
    """Display the main menu"""
    print("\n===== Image Enhancer =====")
    print("1. Load a new image")
    print("2. Apply brightness filter")
    print("3. Save all brightness levels")
    print("4. Apply grayscale filter")
    print("9. Exit")
    return input("Choose an option: ").strip()

def main():
    """Run the main application loop"""
    print("Welcome to Image Enhancer!")
    
    output_dir = "images"
    utils.ensure_dir_exists(output_dir)
    
    current_image, image_path = load_image()
    if current_image is None:
        print("No image loaded. Exiting...")
        return

    while True:
        choice = show_main_menu()

        if choice == "1":
            current_image, image_path = load_image()
        elif choice == "2":
            apply_brightness_filter(current_image, output_dir)
        elif choice == "3":
            save_all_brightness_levels(current_image, output_dir)
        elif choice == "4":
            apply_grayscale_filter(current_image, output_dir)
        elif choice == "9":
            print("Exiting...")
            time.sleep(1)
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()