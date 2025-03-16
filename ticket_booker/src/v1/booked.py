from fastapi import APIRouter, Depends
from core.database import db_connector
from core.config import total_berths
from core.schema import AvailableResponse, AvailableExampleResponse
from typing import Union

router = APIRouter()

# @router.get("/booked")
# def booked(conn = Depends(db_connector)):
#     return {}