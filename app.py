import streamlit as st
import tempfile
from inference import run_image_inference, run_video_inference, avi_to_mp4
from PIL import Image

st.set_page_config(page_title="Mosquito Detection", layout="centered")
st.title("🦟 Mosquito Detection App")

sidebar = st.sidebar
sidebar.title('Model Configuration')

uploaded_file = None

image_or_video = sidebar.radio(
    'Select file type',
    ['Image', 'Video'],
    index=None
)

if image_or_video == 'Video':
    uploaded_file = sidebar.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
elif image_or_video == 'Image':
    uploaded_file = sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
else:
    uploaded_file = None

unit = sidebar.selectbox("Select unit for dimensions", ["Meters", "Centimeters", "Millimeters"])

length = sidebar.number_input("Enter the length of the area", min_value=0.0, step=0.1, format="%.2f")
width = sidebar.number_input("Enter the width of the area", min_value=0.0, step=0.1, format="%.2f")

enable_tracking = sidebar.radio(
    'Enable tracking',
    [True, False],
    index=None
)

if unit == "Centimeters":
    length /= 100
    width /= 100
elif unit == "Millimeters":
    length /= 1000
    width /= 1000

area = length * width
if area <= 0:
    sidebar.warning("Please enter valid dimensions for length and width to calculate the area.")


if image_or_video == 'Image' and uploaded_file is not None:
    image = Image.open(uploaded_file)

    if sidebar.button("Run Image Detection"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_path = temp_file.name

        total_mosquitoes, density, annotated_image = run_image_inference(
            temp_path, length=length, width=width)

        # Show results
        st.subheader("Image Detection Results")

        kpi1, kpi2 = st.columns(2)
        with kpi1:
            st.metric("Total Mosquitoes", total_mosquitoes)
        with kpi2:
            st.metric(f"Density (per sq. {unit.lower()})", f"{density:.2f}")


        col1, col2 = st.columns(2, gap = 'medium', border=True)

        with col1:
            st.subheader("Original Image")
            st.image(image, caption="Original", use_container_width=False)

        with col2:
            st.subheader("Annotated Image")
            st.image(annotated_image, caption="Detection Output", use_container_width=False)

        # Download option
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as img_bytes:
            annotated_image.save(img_bytes.name)
            with open(img_bytes.name, "rb") as f:
                st.download_button(
                    label="Download Annotated Image",
                    data=f,
                    file_name="annotated_result.jpg",
                    mime="image/jpeg"
                )
        st.success("Detection completed successfully!")

elif image_or_video == 'Video' and uploaded_file is not None:
    if sidebar.button("Run Video Detection"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_path = temp_file.name

        # Make sure run_video_inference returns total_mosquitoes, density, and annotated video path
        total_mosquitoes, density, output_video_path = run_video_inference(
            temp_path, enable_tracking=enable_tracking, length=length, width=width)

        # Show results
        st.subheader("Video Detection Results")

        kpi1, kpi2 = st.columns(2)
        with kpi1:
            st.metric("Total Mosquitoes", total_mosquitoes)
        with kpi2:
            st.metric(f"Density (per sq. {unit.lower()})", f"{density:.2f}")

        col1, col2 = st.columns(2, gap='medium', border=True)

        with col1:
            st.subheader("Original Video")
            st.video(uploaded_file, format="video/mp4", start_time=0)

        with col2:
            st.subheader("Annotated Video")
            st.video(avi_to_mp4(output_video_path), format="video/mp4", start_time=0)

        # Download option
        with open(output_video_path, "rb") as f:
            st.download_button(
                label="Download Annotated Video",
                data=f,
                file_name="annotated_result.mp4",
                mime="video/mp4"
            )
        st.success("Detection completed successfully!")
