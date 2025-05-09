import time
import numpy as np
from scipy.signal import convolve2d
import cv2
import matplotlib.pyplot as plt

def old_convolution(image, kernel):
    """Original slow implementation of convolution"""
    # Get image dimensions
    height, width = image.shape[:2]
    kernel_size = kernel.shape[0]
    pad_size = kernel_size // 2
    
    # Pad the image
    padded = np.pad(image, pad_size, mode='symmetric')
    
    # Initialize output
    output = np.zeros_like(image, dtype=np.float32)
    
    # Apply convolution
    for i in range(height):
        for j in range(width):
            # Extract the region of interest
            region = padded[i:i+kernel_size, j:j+kernel_size]
            # Apply the kernel
            output[i, j] = np.sum(region * kernel)
    
    return output

def new_convolution(image, kernel):
    """New optimized implementation using scipy"""
    return convolve2d(image, kernel, mode='same', boundary='symm')

def run_benchmark(image_path, num_runs=3):
    """Run benchmark comparing old and new implementations"""
    # Load and prepare image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    # Sobel kernels
    sobel_x = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])
    
    # Benchmark results
    old_times = []
    new_times = []
    
    print(f"\nRunning benchmark on image: {image_path}")
    print(f"Image size: {image.shape}")
    print(f"Number of runs: {num_runs}")
    print("\nRunning tests...")
    
    for i in range(num_runs):
        # Test old implementation
        start_time = time.time()
        old_result = old_convolution(image, sobel_x)
        old_time = time.time() - start_time
        old_times.append(old_time)
        
        # Test new implementation
        start_time = time.time()
        new_result = new_convolution(image, sobel_x)
        new_time = time.time() - start_time
        new_times.append(new_time)
        
        print(f"\nRun {i+1}:")
        print(f"Old implementation: {old_time:.3f} seconds")
        print(f"New implementation: {new_time:.3f} seconds")
        print(f"Speedup: {old_time/new_time:.1f}x")
    
    # Calculate averages
    avg_old = sum(old_times) / len(old_times)
    avg_new = sum(new_times) / len(new_times)
    
    print("\nResults Summary:")
    print(f"Average time (old): {avg_old:.3f} seconds")
    print(f"Average time (new): {avg_new:.3f} seconds")
    print(f"Average speedup: {avg_old/avg_new:.1f}x")
    
    # Verify results are similar
    mse = np.mean((old_result - new_result) ** 2)
    print(f"\nMean Squared Error between implementations: {mse:.6f}")
    
    # Plot results
    plt.figure(figsize=(12, 4))
    
    # Plot original image
    plt.subplot(131)
    plt.imshow(image, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
    
    # Plot old result
    plt.subplot(132)
    plt.imshow(old_result, cmap='gray')
    plt.title('Old Implementation')
    plt.axis('off')
    
    # Plot new result
    plt.subplot(133)
    plt.imshow(new_result, cmap='gray')
    plt.title('New Implementation')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Test with one of our sample images
    image_path = "images/delft.jpg"
    run_benchmark(image_path) 