# main.py
from fastapi import FastAPI, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import bcrypt
import jwt
from typing import Optional

app = FastAPI()

# MongoDB bağlantısı
MONGO_DETAILS = "mongodb://asmtzl:asmtzl123@194.27.19.117:27017"  # Gerekirse <username> ve <password> yerine kullanıcı adı ve şifreyi koyun
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.plakaDet
users_collection = database.get_collection("user")

SECRET_KEY = "secret_key"  # Bu anahtarı güvenli bir şekilde saklayın

# Pydantic modelleri
class User(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Kullanıcı oluşturma
async def create_user(user: User):
    user_dict = user.dict()
    user_dict["password"] = bcrypt.hashpw(user_dict["password"].encode('utf-8'), bcrypt.gensalt())
    await users_collection.insert_one(user_dict)
    return user

# Kullanıcı doğrulama
async def authenticate_user(username: str, password: str):
    user = await users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return user
    return False

# JWT token oluşturma
def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

# Kayıt Endpoint
@app.post("/register", response_model=User)
async def register(user: User):
    user_in_db = await users_collection.find_one({"username": user.username})
    if user_in_db:
        raise HTTPException(status_code=400, detail="Kullanıcı adı zaten mevcut")
    await create_user(user)
    return user

# Giriş Endpoint
@app.post("/login", response_model=Token)
async def login(user: User):
    authenticated_user = await authenticate_user(user.username, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=400, detail="Geçersiz kullanıcı adı veya şifre")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
