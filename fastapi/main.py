from fastapi import FastAPI, File, UploadFile
from typing import List
from fastapi.responses import JSONResponse
from yolo import detect
import os
from PIL import Image
import numpy as np
import io
from fastapi.middleware.cors import CORSMiddleware
from tempfile import NamedTemporaryFile

# ngrok http --domain=choice-cheetah-rested.ngrok-free.app http://127.0.0.1:8000
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # İzin vermek istediğiniz origin'leri burada belirleyin
    allow_credentials=True,
    allow_methods=["*"],  # İzin vermek istediğiniz metodları burada belirleyin
    allow_headers=["*"],  # İzin vermek istediğiniz başlıkları burada belirleyin
)

"""UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)"""

# Plaka tespiti için kullanacağınız fonksiyonunuzu burada import edin
from yolo import detect

@app.post("/detect_plate/")
async def detect_plate_api(file: UploadFile = File(...)):
   
    contents = await file.read()

    """# Save the uploaded file to the 'uploaded_images' directory
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)"""

    # Görüntüyü aç
    image = Image.open(io.BytesIO(contents))
    # Gerekirse görüntüyü numpy array'e dönüştür
    image_array = np.array(image)
    
    # Plaka tespiti fonksiyonunu kullanarak plakayı bulun
    plate_info = detect(image_array)

    return plate_info

@app.post("/video-detect")
async def detect_faces(file: UploadFile = File(...)):
    temp = NamedTemporaryFile(delete=False)
    try:
        try:
            contents = file.file.read()
            with temp as f:
                f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            file.file.close()
        #process video
        
    except Exception:
        return {"message": "There was an error processing the file"}
    finally:
        #temp.close()  # the `with` statement above takes care of closing the file
        os.remove(temp.name)
        
    return 

@app.get("/detect_plate/")
async def detect_plate_api_get():
   
    return {"send": "post"}

@app.get("/")
async def get_hello():
    return {"message": "Hello!"}

