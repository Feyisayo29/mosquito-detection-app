import os
import numpy as np
import supervision as sv
from ultralytics import YOLO, solutions
from PIL import Image
from pathlib import Path
import shutil
from moviepy import VideoFileClip



def avi_to_mp4(avi_path):
    """Convert AVI video to MP4 format."""
    clip = VideoFileClip(avi_path)
    mp4_path = avi_path.replace('.avi', '.mp4')
    clip.write_videofile(mp4_path, codec='libx264', audio_codec='aac')
    clip.close()
    return mp4_path

def load_model(model_path):
    return YOLO(model_path)

def run_image_inference(image_path, length=None, width=None, confidence_threshold=0.25):
    image = Image.open(image_path)

    if length is None or width is None:
        width, length = image.size  # width, length order from PIL

    image_np = np.array(image)

    model = load_model('model/best.pt')
    results = model.predict(source=image_path, save=False, conf = confidence_threshold)
    detections = sv.Detections.from_ultralytics(results[0])

    bboxes = detections.xyxy
    total_mosquitoes = len(bboxes)

    bounding_box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    labels = [
        model.model.names[class_id]
        for class_id in detections.class_id
    ]

    annotated_image = bounding_box_annotator.annotate(
        scene=image_np, detections=detections)
    annotated_image = label_annotator.annotate(
        scene=annotated_image, detections=detections, labels=labels)
    annotated_image = Image.fromarray(annotated_image)

    density = total_mosquitoes / (length * width)

    return total_mosquitoes, density, annotated_image


def run_video_inference(video_path, enable_tracking=False, length=None, width=None, confidence_threshold=0.25):

    if Path('runs/detect/predict').exists():
        shutil.rmtree('runs/detect/predict')
    model = YOLO("model/best.pt")

    # Run inference
    if enable_tracking:
        results = model.track(source=video_path, save=True, conf = confidence_threshold, persist=True)
    else:
        results = model.predict(source=video_path, save=True, conf = confidence_threshold)

    # Convert results to Supervision detections
    detections = sv.Detections.from_ultralytics(results[0])
    total_mosquitoes = len(detections.xyxy)

    # Avoid division by zero
    if length is None or width is None or length <= 0 or width <= 0:
        density = 0
    else:
        density = total_mosquitoes / (length * width)

    # YOLO saves annotated video inside results[0].save_dir
    save_dir = results[0].save_dir
    filename = os.listdir(save_dir)[0]
    output_video_path = os.path.join(save_dir, filename)
    
    if os.path.exists(output_video_path):
        return total_mosquitoes, density, output_video_path
    else:
        raise FileNotFoundError("Annotated video was not saved correctly.")
