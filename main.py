import os
import time
from filters import apply_brightness, apply_all_brightness_levels, apply_grayscale, add_gaussian_noise, add_salt_pepper_noise
from brightness_helpers import get_brightness_description
import utils
from noise_filter_helper import smooth_image_with_gaussian_blur, smooth_image_with_gaussian_blur, \
    remove_noise_with_median_filter


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


def apply_gaussian_noise_filter(current_image, output_dir):
    """Apply Gaussian noise with user-specified intensity"""
    try:
        intensity = float(input("Enter noise intensity (0.0 to 1.0): "))
        if intensity < 0.0 or intensity > 1.0:
            print("Invalid intensity. Must be between 0.0 and 1.0.")
            return

        result = add_gaussian_noise(current_image, intensity)

        # Save the result
        filename = f"gaussian_noise_{intensity:.2f}.jpg"
        output_path = os.path.join(output_dir, filename)
        utils.save_image(result, output_path)
        print(f"Saved to {output_path}")

        # Display comparison
        title = f"Gaussian Noise (intensity: {intensity:.2f})"
        utils.display_comparison(current_image, result, title)

    except ValueError:
        print("Please enter a value between 0.0 and 1.0.")


def apply_salt_pepper_noise_filter(current_image, output_dir):
    """Apply Salt and Pepper noise with user-specified intensity"""
    try:
        intensity = float(input("Enter noise intensity (0.0 to 1.0): "))
        if intensity < 0.0 or intensity > 1.0:
            print("Invalid intensity. Must be between 0.0 and 1.0.")
            return

        result = add_salt_pepper_noise(current_image, intensity)

        # Save the result
        filename = f"salt_pepper_noise_{intensity:.2f}.jpg"
        output_path = os.path.join(output_dir, filename)
        utils.save_image(result, output_path)
        print(f"Saved to {output_path}")

        # Display comparison
        title = f"Salt and Pepper Noise (intensity: {intensity:.2f})"
        utils.display_comparison(current_image, result, title)

    except ValueError:
        print("Please enter a value between 0.0 and 1.0.")


def denoise_gaussian_filter(current_image, output_dir):
    """Apply Gaussian filter for denoising"""
    try:
        sigma = float(input("Enter sigma value (recommended: 0.5 to 2.0): "))
        if sigma <= 0:
            print("Invalid sigma. Must be greater than 0.")
            return

        result = smooth_image_with_gaussian_blur(current_image, sigma)

        # Save the result
        filename = f"denoised_gaussian_{sigma:.1f}.jpg"
        output_path = os.path.join(output_dir, filename)
        utils.save_image(result, output_path)
        print(f"Saved to {output_path}")

        # Display comparison
        title = f"Gaussian Filter Denoising (sigma: {sigma:.1f})"
        utils.display_comparison(current_image, result, title)

    except ValueError:
        print("Please enter a valid number for sigma.")


def denoise_median_filter(current_image, output_dir):
    """Apply Median filter for denoising"""
    try:
        kernel_size = int(input("Enter kernel size (odd number, recommended: 3, 5, or 7): "))
        if kernel_size < 1 or kernel_size % 2 == 0:
            print("Invalid kernel size. Must be a positive odd number.")
            return

        result = remove_noise_with_median_filter(current_image, kernel_size)

        # Save the result
        filename = f"denoised_median_{kernel_size}.jpg"
        output_path = os.path.join(output_dir, filename)
        utils.save_image(result, output_path)
        print(f"Saved to {output_path}")

        # Display comparison
        title = f"Median Filter Denoising (kernel size: {kernel_size})"
        utils.display_comparison(current_image, result, title)

    except ValueError:
        print("Please enter a valid odd number for kernel size.")


def show_main_menu():
    """Display the main menu"""
    print("\n===== Image Enhancer =====")
    print("1. Load a new image")
    print("2. Apply brightness filter")
    print("3. Save all brightness levels")
    print("4. Apply grayscale filter")
    print("5. Add Gaussian noise")
    print("6. Add Salt and Pepper noise")
    print("7. Denoise with Gaussian filter")
    print("8. Denoise with Median filter")
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
        elif choice == "5":
            apply_gaussian_noise_filter(current_image, output_dir)
        elif choice == "6":
            apply_salt_pepper_noise_filter(current_image, output_dir)
        elif choice == "7":
            denoise_gaussian_filter(current_image, output_dir)
        elif choice == "8":
            denoise_median_filter(current_image, output_dir)
        elif choice == "9":
            print("Exiting...")
            time.sleep(1)
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()