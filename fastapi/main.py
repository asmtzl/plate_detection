from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from yolo import detect
import os , io
from PIL import Image
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from tempfile import NamedTemporaryFile
from pydantic import BaseModel
from hashing import Hash
from typing import Optional
from jwttoken import create_access_token
from oauth import get_current_user

# ngrok http --domain=choice-cheetah-rested.ngrok-free.app http://127.0.0.1:8000
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

from pymongo import MongoClient
mongodb_uri = 'mongodb+srv://asmtzl:pasw@platedet.xlpknrp.mongodb.net/?retryWrites=true&w=majority&appName=plateDet'
port = 8000
client = MongoClient(mongodb_uri, port)
db = client["plateUsers"]

class User(BaseModel):
    username: str
    company: str
    password: str
class Login(BaseModel):
	username: str
	password: str
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: Optional[str] = None

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

@app.post('/register')
def create_user(request:User):
	hashed_pass = Hash.bcrypt(request.password)
	user_object = dict(request)
	user_object["password"] = hashed_pass
	user_id = db["user"].insert_one(user_object)
	# print(user)
	return {"res":"created"}

@app.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends()):
	user = db["user"].find_one({"username":request.username})
	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'No user found with this {request.username} username')
	if not Hash.verify(user["password"],request.password):
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'Wrong Username or password')
	access_token = create_access_token(data={"sub": user["username"] })
	return {"access_token": access_token, "token_type": "bearer"}

