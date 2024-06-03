import string
import easyocr
import json

# Initialize the OCR reader
reader = easyocr.Reader(['en', 'tr'])

def write_json(results, output_path):
 
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4)

def license_complies_format(text):

    return True

def format_license(text):
  
    license_plate_ = ''
    
    for i in range(len(text)): 
        license_plate_ += text[i]

    return license_plate_

def read_license_plate(license_plate_crop):
 
    detections = reader.readtext(license_plate_crop)

    for detection in detections:
        bbox, text, score = detection

        text = text.upper().replace(' ', '')

        if license_complies_format(text):
            return format_license(text), score

    return None, None

def get_car(license_plate, vehicle_track_ids):
   
    x1, y1, x2, y2, score, class_id = license_plate

    foundIt = False
    for j in range(len(vehicle_track_ids)):
        xcar1, ycar1, xcar2, ycar2, car_id = vehicle_track_ids[j]

        if x1 > xcar1 and y1 > ycar1 and x2 < xcar2 and y2 < ycar2:
            car_indx = j
            foundIt = True
            break

    if foundIt:
        return vehicle_track_ids[car_indx]

    return -1, -1, -1, -1, -1
