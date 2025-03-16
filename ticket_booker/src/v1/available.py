from fastapi import APIRouter, Depends
from core.database import db_connector
from core.config import total_berths
from core.schema import AvailableResponse, AvailableExampleResponse
from typing import Union

router = APIRouter()

@router.get("/available", 
            response_model = AvailableResponse,
            responses = AvailableExampleResponse
        )
def available(conn = Depends(db_connector)):
    cursor = conn.cursor()
    cursor.execute("SELECT berth_type, COUNT(1) as booked FROM passengers WHERE is_cancelled != true GROUP BY berth_type")
    available = {berth_type: total_berths[berth_type]-booked_count for berth_type, booked_count in cursor.fetchall() }
    cursor.close()
    return available