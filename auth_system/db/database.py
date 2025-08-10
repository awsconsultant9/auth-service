from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from auth_system.schema.models import UserRegistration, RoleCreate, UserLogin
from auth_system.models.user import User, Role, UserRole
from auth_system.utils.security import hash_password, verify_password
import asyncio
from sqlalchemy import create_engine, select


DEFAULT_ROLE = "cc24addf-73d8-455f-b69d-4b59b10f004b"
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/jwtservice"
DATABASE_URL_SYNC = "postgresql://postgres:postgres@localhost:5432/jwtservice"


engine = create_async_engine(DATABASE_URL, echo=True)
sessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
class UserNotFound(Exception):
    pass

async def get_db():
    async with sessionLocal() as session:
        yield session

engine_sync = create_engine(DATABASE_URL_SYNC, echo=True)
SyncSessionLocal = sessionmaker(bind=engine_sync)

def get_sync_db():
    with SyncSessionLocal() as session:
        yield session


async def registration(userinfo:UserRegistration, db:AsyncSession):
    hashed_password = await asyncio.to_thread(hash_password, userinfo.password)
    db_user = User(**userinfo.dict(exclude={"password"}), password=hashed_password)
    try:
        db.add(db_user)
        await db.flush()
        user_role = UserRole(user_id=db_user.id, role_id=DEFAULT_ROLE)
        db.add(user_role)
        await db.commit()
        await db.refresh(db_user)
    except Exception as e :
        await db.rollback()
        raise e
    return db_user

def create_role(role:RoleCreate,db:Session):
    db_role = Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


async def login(credentials:UserLogin, session:AsyncSession):

    stmt = select(User).where(User.email==credentials.email)
    user = (await session.execute(stmt)).scalars().one_or_none()
    if user:
        if verify_password(credentials.password, user.password):
            subquery = select(UserRole.role_id).where(UserRole.user_id==user.id)
            stmt = select(Role.name).where(Role.id.in_(subquery))
            roles = (await session.execute(stmt)).scalars().all()
            return roles

    raise UserNotFound()
