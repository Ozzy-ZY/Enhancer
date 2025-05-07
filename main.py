# ToDo: add an Interactive-CLI to be facing the user

import os
import time

from filters import BrightnessFilter, GrayscaleFilter
import utils


class ImageEnhancer:
    """Main application for image enhancement"""

    def __init__(self):
        self.filters = {
            "brightness": BrightnessFilter(),
            "grayscale": GrayscaleFilter(),
            # Add more filters here as you develop them
        }
        self.output_dir = "images"
        utils.ensure_dir_exists(self.output_dir)
        self.current_image = None
        self.image_path = None

    def load_image(self):
        """Prompt user for image path and load it"""
        while True:
            try:
                path = input("Path to input image\n(example: images/delft.jpg) : ").strip()
                self.current_image = utils.load_image(path)
                self.image_path = path
                print(f"Image loaded successfully: {path}")
                return True
            except (FileNotFoundError, IOError) as e:
                print(f"Error: {e}")
                retry = input("Try again? (y/n): ").strip().lower()
                if retry != 'y':
                    return False

    def apply_brightness_filter(self):
        """Apply brightness filter with user-specified level"""
        brightness_filter = self.filters["brightness"]
        try:
            level = int(input("Enter brightness level (-4 to 4): "))
            if level not in brightness_filter.levels:
                print("Invalid level. Must be between -4 and 4.")
                return

            result = brightness_filter.apply(self.current_image, level)

            # Save the result
            filename = f"brightness_{level:+d}.jpg"
            output_path = os.path.join(self.output_dir, filename)
            utils.save_image(result, output_path)
            print(f"Saved to {output_path}")

            # Display comparison
            title = f"Brightness level {level:+d} ({brightness_filter.get_level_description(level)})"
            utils.display_comparison(self.current_image, result, title)

        except ValueError:
            print("Please enter a number between -4 and 4.")

    def save_all_brightness_levels(self):
        """Save all brightness adjustment levels"""
        brightness_filter = self.filters["brightness"]
        results = brightness_filter.apply_all_levels(self.current_image)

        for level, image in results.items():
            filename = f"brightness_{level:+d}.jpg"
            output_path = os.path.join(self.output_dir, filename)
            utils.save_image(image, output_path)

        print(f"All brightness levels saved to {self.output_dir}/")

    def apply_grayscale_filter(self):
        """Apply grayscale filter"""
        grayscale_filter = self.filters["grayscale"]
        result = grayscale_filter.apply(self.current_image)

        # Save the result
        output_path = os.path.join(self.output_dir, "grayscale.jpg")
        utils.save_image(result, output_path)
        print(f"Saved to {output_path}")

        # Display comparison
        utils.display_comparison(self.current_image, result, "Grayscale")

    def show_main_menu(self):
        """Display the main menu"""
        print("\n===== Image Enhancer =====")
        print("1. Load a new image")
        print("2. Apply brightness filter")
        print("3. Save all brightness levels")
        print("4. Apply grayscale filter")
        # Add more menu options as you add filters
        print("9. Exit")
        return input("Choose an option: ").strip()

    def run(self):
        """Run the main application loop"""
        print("Welcome to Image Enhancer!")

        if not self.load_image():
            print("No image loaded. Exiting...")
            return

        while True:
            choice = self.show_main_menu()

            if choice == "1":
                self.load_image()
            elif choice == "2":
                self.apply_brightness_filter()
            elif choice == "3":
                self.save_all_brightness_levels()
            elif choice == "4":
                self.apply_grayscale_filter()
            elif choice == "9":
                print("Exiting...")
                time.sleep(1)
                break
            else:
                print("Invalid option.")


if __name__ == "__main__":
    enhancer = ImageEnhancer()
    enhancer.run()