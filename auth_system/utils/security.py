from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta



pwd_context = CryptContext(schemes=["bcrypt", "argon2"], deprecated="auto")

SECRET_KEY = "peddy"
ALGORITHM = "HS256"
TOKEN_EXPIRY_IN_MINUTES = 60

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(text_password:str, hashed_password:str):
    return pwd_context.verify(text_password,hashed_password)

def create_access_token(payload:dict):
    expire = datetime.utcnow()+timedelta(minutes=TOKEN_EXPIRY_IN_MINUTES)
    payload.update({"exp":expire})
    access_token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return access_token