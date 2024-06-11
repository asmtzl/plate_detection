import numpy as np
import cv2 as cv
from ultralytics import YOLO
from sort.sort import *
from read import get_car, read_license_plate, write_json

def read_video(video_path):
    cap = cv.VideoCapture(video_path)
    return cap

def detect_objects_yolo(model, frame, classes):
    detections = model(frame)[0]
    detections_ = []
    for detection in detections.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = detection
        if int(class_id) in classes:
            detections_.append([x1, y1, x2, y2, score])
    return detections_

def track_objects(detections, tracker):
    track_ids = tracker.update(np.asarray(detections))
    return track_ids

def detect_license_plates(model, frame):
    license_plates = model(frame)[0]
    return license_plates

def crop_license_plate(frame, license_plate_bbox):
    x1, y1, x2, y2, _, _ = license_plate_bbox
    license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]
    return license_plate_crop

def process_license_plate(license_plate_crop):
    license_plate_crop_gray = cv.cvtColor(license_plate_crop, cv.COLOR_BGR2GRAY)
    _, license_plate_crop_thresh = cv.threshold(license_plate_crop_gray, 64, 255, cv.THRESH_BINARY_INV)
    return license_plate_crop_thresh

def process_frame(frame, coco_model, license_plate_model, mot_tracker):
    results = {}
    vehicles = [2, 3, 5, 7]

    detections = detect_objects_yolo(coco_model, frame, vehicles)
    track_ids = track_objects(detections, mot_tracker)

    license_plates = detect_license_plates(license_plate_model, frame)

    for license_plate in license_plates.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = license_plate
        xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

        if car_id != -1:
            license_plate_crop = crop_license_plate(frame, license_plate)
            license_plate_crop_thresh = process_license_plate(license_plate_crop)
            license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)

            if license_plate_text is not None:
                results[car_id] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                                   'license_plate': {'bbox': [x1, y1, x2, y2],
                                                     'text': license_plate_text,
                                                     'bbox_score': score,
                                                     'text_score': license_plate_text_score}}
    return results

def process_video(video_path, coco_model, license_plate_model, mot_tracker):
    cap = read_video(video_path)
    frame_nmr = -1
    ret = True
    results = {}

    while ret:
        frame_nmr += 1
        ret, frame = cap.read()
        if ret:
            results[frame_nmr] = process_frame(frame, coco_model, license_plate_model, mot_tracker)
    cap.release()
    return results

if __name__ == "__main__":
    coco_model = YOLO('E:/VS Code Projects/plate_detection/fastapi/model/yolov8n.pt')
    license_plate_model = YOLO('E:/VS Code Projects/plate_detection/fastapi/model/best2.pt')
    mot_tracker = Sort()
    video_path = 'C:/yolov88/opencvstudy/plakaoku.mp4'
    results = process_video(video_path, coco_model, license_plate_model, mot_tracker)
    write_json(results, './testdeneme.json')
