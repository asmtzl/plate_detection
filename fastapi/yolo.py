import torch
import numpy as np
import cv2 
import easyocr
from ultralytics import YOLO
import json
from fastapi.responses import JSONResponse

#model = torch.hub.load('E:/VS Code Projects/Py/fastapitry/model/best.pt', 'custom', path='E:/VS Code Projects/Py/fastapitry/model/best.pt', source='local')
#model = torch.load('E:/VS Code Projects/Py/fastapi/fastapitry/model/best.pt')


def detect(image):
    target_size=(640,640)
    pre_im = image
    #pre_im = cv2.resize(image, target_size)
    #pre_im = cv2.GaussianBlur(pre_im, (3, 3), 0)
    """cv2.imshow('prep',pre_im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()"""
    model = YOLO('E:/VS Code Projects/plate_detection/fastapi/model/best2.pt')
    #model = torch.load('E:/VS Code Projects/Py/fastapitry/model/best.pt')
    #prediction_json = model.predict(small, confidence=40, overlap=30).json()
    results = model.predict(pre_im, conf=0.40, iou=0.30)
    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs
        print(boxes)
        bounding_box = boxes.xyxy
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        obb = result.obb  # Oriented boxes object for OBB outputs
        #result.show()  # display to screen
    

    img = pre_im
    
    for box in bounding_box:
        x0 = int(box[0])
        x1 = int(box[2])
        y0 = int(box[1])
        y1 = int(box[3])
        
        start_point = (int(x0), int(y0))
        end_point = (int(x1), int(y1))
        img = cv2.rectangle(img, start_point, end_point, color=(0,255,0), thickness=2)
        plate = img[y0:y1,x0:x1]

    """cv2.imshow('plate',plate)
    cv2.waitKey(0)
    cv2.destroyAllWindows()  """
    
    if plate is None:
            return JSONResponse(content={"error": "No bounding boxes found."}, status_code=404)


    gray_plate = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
 
    reader = easyocr.Reader(['en'])
    result = reader.readtext(gray_plate)
    plate_text = []
    for (bbox, text, prob) in result:
        print(f'Text: {text}, Probability: {prob}')
        plate_text.append(text)
    plate_json = json.dumps(plate_text)
    combined = "".join(plate_text)
    return combined
   
"""image_path = "C:/Users/Acer/Desktop/plate_images/1.jpg"
image = cv2.imread(image_path)
res = detect(image)
print(res)"""

def framesFromVid(path):
    readed_frames = []
    vidcap = cv2.VideoCapture(path)
    success,image = vidcap.read()
    count = 0
    while success:
        readed_frames.append(image) 
        success,image = vidcap.read()
        count += 1
    print("readed frames :",count)
    return readed_frames

