from fastapi import APIRouter, FastAPI
from src.v1 import router as v1_router

app = FastAPI()
app.include_router(v1_router)

