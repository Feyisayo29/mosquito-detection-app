# Mosquito Detection App

This project is a web-based application for detecting and counting mosquitoes in images and videos using a YOLO-based deep learning model. The app provides an easy-to-use interface for uploading images or videos, running detection, and downloading annotated results. It also calculates the density of detected mosquitoes per unit area.

---

## Features

- **Image and Video Detection:** Upload images (`.jpg`, `.jpeg`, `.png`) or videos (`.mp4`, `.avi`, `.mov`) for mosquito detection.
- **Density Calculation:** Computes mosquito density based on user-specified area dimensions and units (meters, centimeters, millimeters).
- **Annotation and Download:** View and download annotated images or videos with bounding boxes and labels.
- **Tracking Option:** Optionally enable object tracking for videos.
- **User-Friendly Interface:** Built with [Streamlit](https://streamlit.io/) for interactive web-based usage.

---

## Repository Structure

```
.
├── app.py                   # Main Streamlit app
├── inference.py             # Inference logic for images and videos
├── main.py                  # (Empty or for future CLI/entrypoint)
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
├── images/                  # Example input images
│   ├── image_13_7.jpg
│   └── ...
├── model/
│   └── best.pt              # Trained YOLO model weights
├── videos/                  # Example input videos
│   ├── video1.mp4
└── __pycache__/             # Python cache files
```

---

## Installation

### 1. Clone the Repository

```sh
git clone https://github.com/Feyisayo29/mosquito-detection-app.git
cd mosquito-detection-app
```

### 2. Set Up a Python Environment

It is recommended to use a virtual environment:

```sh
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

Install all required Python packages:

```sh
pip install -r requirements.txt
```

**Note:**  
- Make sure you have Python 3.8+ installed.
- The model weights file should be present at `model/best.pt`. If not, place your trained YOLO model there.

---

## Usage

### 1. Run the Streamlit App

```sh
streamlit run app.py
```

This will launch the app in your default web browser.

### 2. Using the App

- **Select File Type:** Choose between "Image" or "Video".
- **Upload File:** Upload your image or video file.
- **Set Area Dimensions:** Enter the length and width of the area in your preferred unit (meters, centimeters, or millimeters).
- **Enable Tracking (Video Only):** Optionally enable object tracking for videos.
- **Run Detection:** Click the detection button to process your file.
- **View Results:** See the total mosquito count, density, and annotated output.
- **Download:** Download the annotated image or video.

---

## Notes

- The app uses a YOLO model trained for mosquito detection. For best results, use images/videos similar to your training data.
- Annotated outputs are saved temporarily and can be downloaded directly from the app.
- For video detection, the app may take some time depending on video length and system performance.

---

## Troubleshooting

- **Model Not Found:** Ensure `model/best.pt` exists.
- **Dependency Issues:** Double-check your Python version and installed packages.

---

## License

This project is for educational and research purposes. Please check the individual licenses of dependencies and the YOLO model.

---

## Acknowledgements

- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)
- [Supervision](https://github.com/roboflow/supervision)

- [Streamlit](https://streamlit.io/)
