
from auth_system.schema.models import UserRegistration, RoleCreate, UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from auth_system.db import database
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from auth_system.utils.security import create_access_token

async def registration(userinfo:UserRegistration, db:AsyncSession):
    return await database.registration(userinfo,db)

def create_role(role:RoleCreate,db:Session):
    return database.create_role(role,db)


async def login(credentials:UserLogin, db:AsyncSession):
    try:
        roles = await database.login(credentials,db)
    except database.UserNotFound:
        raise HTTPException(status_code=404, detail="User not Found")
    return create_access_token({"claims":roles})



