from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from auth_system.schema.models import UserRegistration, UserResponse, RoleCreate, UserLogin
from auth_system.db.database import get_db, get_sync_db
from auth_system.services import auth_service
from auth_system.utils.security import create_access_token, verify_token_extract_claims

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

@router.get("/protected")
def protected_route(request:Request):
    auth_header = request.headers.get("Authorization")
    if auth_header is None or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing or invalid auth header")
    token = auth_header[len("Bearer "):]
    claims = verify_token_extract_claims(token)
    return claims