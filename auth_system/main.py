from fastapi import FastAPI
from auth_system.router.auth_router import router
app = FastAPI()

app.include_router(router)