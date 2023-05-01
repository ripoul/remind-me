from fastapi import FastAPI, Request, Response

from auth import auth
from database import engine, SessionLocal
import models

app = FastAPI()
app.include_router(auth.router)
models.Base.metadata.create_all(bind=engine)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.get("/")
def read_root():
    return {"Hello": "World"}
