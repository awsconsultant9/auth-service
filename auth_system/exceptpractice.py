from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from auth_system.logging import config
config.log_configuring()
import logging
logger = logging.getLogger(__name__)


class NXPException(Exception):
    def __init__(self, detail, status_code=401):
        self.detail = detail
        self.status_code = status_code

class InsufficientFunds(NXPException):
    pass

class AccountFrozen(NXPException):
    pass

app = FastAPI()
@app.exception_handler(NXPException)
def business_exception_handler(request:Request, exc:NXPException):
    return JSONResponse(status_code=exc.status_code,
                        content={"error":exc.detail})

@app.get("/withdraw")
def withdraw():
    raise InsufficientFunds(detail="if you hit this end point it always raise insufficient funds", status_code=404)

@app.get("/frozen")
def frozen():
    logger.info("frozen exception is raised")
    raise AccountFrozen(detail="if you hit this end point it always raise account frozen")


