from fastapi import APIRouter, Depends, Path
from core.database import db_connector
from fastapi.responses import JSONResponse
from core.schema import BookedResponse, BookedExampleResponse, BookingDetailsResponse
import psycopg2.extras 

router = APIRouter()

@router.get("/booked", response_model=BookedResponse, responses = BookedExampleResponse)
def booked_tickets(conn = Depends(db_connector)):
    cursor = conn.cursor()
    cursor.execute("SELECT berth_type, COUNT(1) as booked FROM passengers WHERE is_cancelled == false GROUP BY berth_type")
    available_data= {berth_type: booked_count for berth_type, booked_count in cursor.fetchall() }
    cursor.close()
    return JSONResponse(status_code = 200, content = available_data)


@router.get("/booked/{booking_id}", response_model=BookingDetailsResponse)
def booked_details(conn = Depends(db_connector), booking_id: str = Path(..., regex="^PNR[0-9]{5}$"), description="booking_id is a string with 8 charc length, should start with PNR case senstive, followe by 5 digit number"):
    print("in booked api",booking_id)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT b.pnr, b.booked_by, b.source, b.destination, b.travel_date, b.created_at, \
                   p.name, p.age, p.gender, p.berth_type FROM bookings as b LEFT JOIN passengers as p on b.pnr = p.pnr where b.pnr = %s", (booking_id,))
    data = cursor.fetchall()
    booking_data = {
        "booking_id": data[0]["pnr"],
        "booked_user": data[0]["booked_by"],
        "from_location": data[0]["source"],
        "to_location": data[0]["destination"],
        "departure_date": data[0]["travel_date"],
        "booked_on": data[0]["created_at"],
        "passenger_details": [
            {
                "name": passenger["name"],
                "age":passenger["age"],
                "gender":passenger["gender"],
                "berth_type": passenger["berth_type"],
                "berth_no": passenger["berth_no"]
            }
            for passenger in data
        ] 
    }
    cursor.close()
    if booking_data:
        return JSONResponse(status_code = 200, content = booking_data)
    else:
        return JSONResponse(status_code = 404, content = {"message": "booking details not found"})