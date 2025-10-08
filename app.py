import streamlit as st
import tempfile
from inference import run_image_inference, run_video_inference, avi_to_mp4
from PIL import Image
from risk_analysis import get_risk_metrics

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

# Convert to meters for risk calculation
length_m = length
width_m = width
if unit == "Centimeters":
    length_m = length / 100
    width_m = width / 100
elif unit == "Millimeters":
    length_m = length / 1000
    width_m = width / 1000

area = length_m * width_m
if area <= 0:
    sidebar.warning("Please enter valid dimensions for length and width to calculate the area.")


if image_or_video == 'Image' and uploaded_file is not None:
    image = Image.open(uploaded_file)

    if sidebar.button("Run Image Detection"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_path = temp_file.name

        total_mosquitoes, density, annotated_image = run_image_inference(
            temp_path, length=length_m, width=width_m)

        # Calculate risk metrics
        risk_metrics = get_risk_metrics(total_mosquitoes, area)

        # Show results
        st.subheader("Image Detection Results")

        # Display risk assessment with color coding
        st.markdown(f"""
        <div style="padding: 20px; border-radius: 10px; background-color: {risk_metrics['color']}15; 
                    border: 2px solid {risk_metrics['color']}; margin: 20px 0;">
            <h2 style="color: {risk_metrics['color']}; margin-bottom: 10px;">
                {risk_metrics['emoji']} Risk Assessment: {risk_metrics['risk_level']}
            </h2>
            <p style="font-size: 16px; margin: 10px 0; color: #333;">
                {risk_metrics['description']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1:
            st.metric("Total Mosquitoes", total_mosquitoes)
        with kpi2:
            st.metric(f"Density (per sq. {unit.lower()})", f"{density:.2f}")
        with kpi3:
            st.metric("Density (per m²)", f"{risk_metrics['density']:.2f}")

        col1, col2 = st.columns(2, gap='medium', border=True)

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
            temp_path, enable_tracking=enable_tracking, length=length_m, width=width_m)

        # Calculate risk metrics
        risk_metrics = get_risk_metrics(total_mosquitoes, area)

        # Show results
        st.subheader("Video Detection Results")

        # Display risk assessment with color coding
        st.markdown(f"""
        <div style="padding: 20px; border-radius: 10px; background-color: {risk_metrics['color']}15; 
                    border: 2px solid {risk_metrics['color']}; margin: 20px 0;">
            <h2 style="color: {risk_metrics['color']}; margin-bottom: 10px;">
                {risk_metrics['emoji']} Risk Assessment: {risk_metrics['risk_level']}
            </h2>
            <p style="font-size: 16px; margin: 10px 0; color: #333;">
                {risk_metrics['description']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1:
            st.metric("Total Mosquitoes", total_mosquitoes)
        with kpi2:
            st.metric(f"Density (per sq. {unit.lower()})", f"{density:.2f}")
        with kpi3:
            st.metric("Density (per m²)", f"{risk_metrics['density']:.2f}")

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

# Add information section at the bottom
st.markdown("---")
with st.expander("ℹ️ About Risk Levels"):
    st.markdown("""
    ### Risk Level Definitions
    
    **🟢 Low Risk (< 0.5 mosquitoes/m²)**
    - Minimal disease transmission potential
    - Continue regular monitoring
    - Standard preventive measures sufficient
    
    **🟡 Medium Risk (0.5 - 2.0 mosquitoes/m²)**
    - Moderate disease transmission risk
    - Consider implementing control measures
    - Increase monitoring frequency
    - Remove standing water sources
    
    **🔴 High Risk (> 2.0 mosquitoes/m²)**
    - High disease transmission potential
    - Immediate intervention recommended
    - Contact local vector control authorities
    - Implement comprehensive mosquito control
    - Use personal protective measures
    
    ### Scientific Basis
    
    These thresholds are based on research on mosquito-borne disease transmission,
    particularly for species like *Aedes aegypti* that transmit dengue, Zika, and chikungunya.
    
    Research has shown that:
    - Densities below 1-3 females per trap per week represent relatively safe levels
    - Higher densities significantly increase disease transmission risk
    - Immediate control measures are needed when mosquito populations exceed critical thresholds
    
    **Note:** Actual disease risk also depends on mosquito species, virus prevalence in the area,
    environmental conditions, and human population density.
    """)
