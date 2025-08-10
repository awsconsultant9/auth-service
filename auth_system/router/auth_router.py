from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from auth_system.schema.models import UserRegistration, UserResponse, RoleCreate, UserLogin
from auth_system.db.database import get_db, get_sync_db
from auth_system.services import auth_service

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def registration(userinfo:UserRegistration, db=Depends(get_db)):
    return await auth_service.registration(userinfo,db)

@router.post("/role")
def create_role(role:RoleCreate, db:Session=Depends(get_sync_db)):
    return auth_service.create_role(role, db)

@router.post("/login")
async def login(credentials:UserLogin, db:AsyncSession=Depends(get_db)):
    return await auth_service.login(credentials,db)