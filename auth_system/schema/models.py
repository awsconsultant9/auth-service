from pydantic import BaseModel, EmailStr
import uuid
from datetime import datetime

class UserRegistration(BaseModel):
    name: str
    password: str
    email: EmailStr

class UserResponse(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime

class RoleCreate(BaseModel):
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

