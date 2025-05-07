import os
import time

import cv2
import numpy as np
import matplotlib.pyplot as plt

def adjust_brightness(image, factor):
    return np.clip(image * factor, 0, 255).astype(np.uint8)

def save_image(img, path):
    cv2.imwrite(path, img)

def main():
    brightness_levels = {
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

    input_path = input("Path to input image \n(example: images/delft.jpg) : ").strip()
    if not os.path.isfile(input_path):
        print("File not found.")
        return

    image = cv2.imread(input_path)
    if image is None:
        print("Could not open image.")
        return

    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)

    while True:
        print("\n1. Apply brightness level")
        print("2. Save all brightness levels")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            try:
                level = int(input("Enter brightness level (-4 to 4): "))
                if level not in brightness_levels:
                    print("Invalid level.")
                    continue
                factor = brightness_levels[level]
                result = adjust_brightness(image, factor)

                filename = f"adjusted_{level:+d}.jpg"
                path = os.path.join(output_dir, filename)
                save_image(result, path)
                print(f"Saved to {path}")

                # Show comparison
                plt.subplot(1, 2, 1)
                plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                plt.title("Original Image")
                plt.axis('off')

                plt.subplot(1, 2, 2)
                plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
                plt.title(f"Brightness level {level:+d}")
                plt.axis('off')

                plt.show()
            except ValueError:
                print("Enter a number between -4 and 4.")

        elif choice == "2":
            for lvl, factor in brightness_levels.items():
                if lvl == 0:
                    continue
                adj = adjust_brightness(image, factor)
                fname = f"adjusted_{lvl:+d}.jpg"
                save_image(adj, os.path.join(output_dir, fname))
            print("All versions saved in images folder.")

        elif choice == "3":
            print("Exiting...")
            time.sleep(2)
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
