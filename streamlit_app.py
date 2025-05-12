import streamlit as st
import numpy as np
from PIL import Image
import io
from Quantitative_Proof import sobel_gradient_energy,variance_of_laplacian

from filters import (
    apply_brightness, apply_all_brightness_levels, apply_grayscale,
    add_gaussian_noise, add_salt_pepper_noise, apply_edge_detection, unsharp_mask, apply_channel_swap
)
from brightness_helpers import get_brightness_description
from noiseRemovalFilter import remove_noise
from InvertColorFilter import apply_invert
from noise_filter_helper import smooth_image_with_gaussian_blur, remove_noise_with_median_filter

st.set_page_config(page_title="Image Enhancer", layout="wide")
st.title("🖼️ Enhancer")

# Load image uploader
uploaded_file = st.sidebar.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

PREVIEW_WIDTH = 400  # Adjust this value for smaller or larger previews

if uploaded_file:
    pil_img = Image.open(uploaded_file)
    img = np.array(pil_img)

    # Show original image at a fixed width
    st.image(pil_img, caption="Original Image", width=PREVIEW_WIDTH)

    operation = st.sidebar.selectbox("Choose Operation", [
        "None/Preview",
        "Brightness",
        "Grayscale",
        "Add Gaussian Noise",
        "Add Salt & Pepper Noise",
        "Denoise (Gaussian)",
        "Denoise (Median)",
        "Noise Removal Tool",
        "Invert Colors",
        "Edge Detection",
        "Image Sharpening"
    ])

    result = img.copy()
    out_filename = "output.jpg"

    if operation == "Brightness":
        lvl = st.sidebar.slider("Brightness Level", -4, 4, 0)
        result = apply_brightness(img, lvl)
        out_filename = f"brightness_{lvl:+d}.jpg"
        st.caption(f"Brightness level {lvl} ({get_brightness_description(lvl)})")

    elif operation == "Grayscale":
        result = apply_grayscale(img)
        out_filename = "grayscale.jpg"

    elif operation == "Add Gaussian Noise":
        intensity = st.sidebar.slider("Gaussian Noise Intensity", 0.0, 1.0, 0.2)
        result = add_gaussian_noise(img, intensity)
        out_filename = f"gaussian_{intensity:.2f}.jpg"

    elif operation == "Add Salt & Pepper Noise":
        intensity = st.sidebar.slider("Salt & Pepper Intensity", 0.0, 1.0, 0.2)
        result = add_salt_pepper_noise(img, intensity)
        out_filename = f"saltpep_{intensity:.2f}.jpg"

    elif operation == "Denoise (Gaussian)":
        sigma = st.sidebar.slider("Gaussian Sigma", 0.5, 2.0, 1.0)
        result = smooth_image_with_gaussian_blur(img, sigma)
        out_filename = f"denoised_gaussian_{sigma:.1f}.jpg"

    elif operation == "Denoise (Median)":
        kernel = st.sidebar.select_slider("Median Kernel Size", options=[3, 5, 7], value=3)
        result = remove_noise_with_median_filter(img, kernel)
        out_filename = f"denoised_median_{kernel}.jpg"

    elif operation == "Noise Removal Tool":
        method = st.sidebar.radio("Method", ["Median", "Gaussian", "Bilateral"])
        if method == "Median":
            result = remove_noise(img, method="median", ksize=5)
            out_filename = "denoised_median.jpg"
        elif method == "Gaussian":
            result = remove_noise(img, method="gaussian", ksize=(5, 5), sigma=0)
            out_filename = "denoised_gaussian.jpg"
        else:
            result = remove_noise(img, method="bilateral", d=9, sigma_color=75, sigma_space=75)
            out_filename = "denoised_bilateral.jpg"

    elif operation == "Invert Colors":
        result = apply_invert(img)
        out_filename = "inverted.jpg"

    elif operation == "Edge Detection":
        edge_dir = st.sidebar.selectbox("Direction", ["horizontal", "vertical", "both"])
        sensitivity = st.sidebar.slider("Sensitivity", 0.1, 2.0, 1.0)
        result = apply_edge_detection(img, sensitivity, edge_dir)
        out_filename = f"edges_{edge_dir}_{sensitivity:.1f}.jpg"


    elif operation == "Image Sharpening":

        ksize = st.sidebar.slider("Kernel Size (odd)", 3, 15, 5, step=2)

        sigma = st.sidebar.slider("Gaussian Sigma", 0.1, 5.0, 1.0)

        amount = st.sidebar.slider("Sharpen Amount", 0.1, 3.0, 1.5)

        threshold = st.sidebar.slider("Threshold", 0, 50, 10)

        result = unsharp_mask( img,ksize=(ksize, ksize), sigma=sigma,amount=amount,threshold=threshold )

        out_filename = f"sharpen_k{ksize}_σ{sigma:.1f}_a{amount:.1f}_t{threshold}.jpg"
        # Compute verification metrics
        fm_orig = variance_of_laplacian(img)
        fm_sharp = variance_of_laplacian(result)
        se_orig = sobel_gradient_energy(img)
        se_sharp = sobel_gradient_energy(result)

        # Show result
        st.image(result, caption="Result: Sharpen", width=PREVIEW_WIDTH)
        st.markdown("**🔍 Focus Metrics**")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Variance of Laplacian", f"{fm_sharp:.2f}", delta=f"{fm_sharp - fm_orig:.2f}")
        with c2:
            st.metric("Sobel Energy", f"{se_sharp:.0f}", delta=f"{se_sharp - se_orig:.0f}")

    else:
        st.info("Choose an operation from the sidebar to process your image!")

    # Show and Download Result
    if operation != "None/Preview":
        # Show result image at the same fixed width
        st.image(result, caption=f"Result: {operation}", width=PREVIEW_WIDTH)

        buf = io.BytesIO()
        Image.fromarray(result.astype(np.uint8)).save(buf, format="JPEG")
        st.download_button("Download Result", buf.getvalue(), file_name=out_filename, mime="image/jpeg")
else:
    st.info("Please upload an image to get started!")
