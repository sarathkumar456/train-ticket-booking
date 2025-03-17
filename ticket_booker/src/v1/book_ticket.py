from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from core.database import db_connector
from core.schema import BookingRequestBody
from core.config import IST
from datetime import datetime
import random
import psycopg2.extras

router = APIRouter()

@router.post("/book")
def book_ticket(request: BookingRequestBody, conn=Depends(db_connector)):
    pnr = f"PNR{str(int(datetime.now(IST).timestamp()*1000))[-5:]}"
    booked_by, source, destination, travel_date = request.booked_by, request.source, request.destination, request.travel_date
    updated_berth_ids = []
    passengers = [passenger for passenger in request.passenger_details if passenger['age'] >= 60]+[passenger for passenger in request.passenger_details if (passenger["gender"] == "female" and passenger["children"])] + [passenger for passenger in request.passenger_details if not ((passenger["gender"] == "female" and passenger["children"]) or (passenger["age"] >= 60))]
    passengers_berth_info = []
    for passenger in passengers:
        cursor = conn.cursor()
        name, age, gender, children = passenger["name"], passenger["age"], passenger["gender"], passenger["children"]
        cursor.execute("SELECT id, berth_type, berth_no FROM berth_map WHERE occupied = false ORDER BY id asc LIMIT 1 FOR UPDATE SKIP LOCKED")
        berth = cursor.fetchone(cursor_factory=psycopg2.extras.RealDictCursor)
        if berth:
            cursor.execute("""
                            UPDATE berth_map SET occupied = true WHERE berth_no = %s
                            """, (berth["berth_no"],))
            updated_berth_ids.append(cursor.fetchone()[0])            
            cursor.execute(
                """
                INSERT INTO passengers (pnr, name, age, gender, berth_type, berth_no, gaurdian_id) VALUES
                (%s, %s, %s, %s, %s, %s)
                """,
                (pnr, name, age, gender, berth["berth_type"], berth["berth_no"], None,)
            )
            passengers_berth_info.append({"name": name, "age": age, "gender": gender, "berth_type": berth["berth_type"], "berth_no": berth["berth_no"]})
            gaurdian_id = cursor.fetchone()[0]
            childrens_insertion_data = []
            if children:
                for child in children:
                    childrens_insertion_data.append((pnr, child['name'], child['age'], child['gender'], berth["berth_type"], berth["berth_no"], gaurdian_id,))
                    passengers_berth_info.append({"name": child['name'], "age": child['age'], "gender": child['gender'], "berth_type": berth["berth_type"], "berth_no": berth["berth_no"], "is_child": True, "gaurdian_name": name})
                    
                cursor.executemany(
                    """
                    INSERT INTO passengers (pnr, name, age, gender, berth_type, berth_no, gaurdian_id) VALUES
                    (%s, %s, %s, %s, %s, %s)
                    """,
                    childrens_insertion_data
                )
            conn.commit()
        else:
            if updated_berth_ids:
                cursor.execute(
                    """
                    UPDATE berth_map SET occupied = false WHERE berth_no IN %s
                    """, (updated_berth_ids,)
                )
                conn.commit()
                cursor.execute("DELETE FROM passengers WHERE pnr = %s", (pnr, ))
                conn.commit()
                updated_berth_ids = []
                cursor.close()
                break
                
        
    if not updated_berth_ids:
        return JSONResponse(status_code = 404, description = "No tickets Available") 
    else:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO bookings (pnr, booked_by, source, destination, travel_date) VALUES 
            (%s, %s, %s, %s, %s)
            """,
            (pnr, booked_by, source, destination, travel_date)
        )
        booked_details_response = {
            "pnr": pnr, "booked_by": booked_by, "source": source, "destination": destination, "travel_date": travel_date,
            "passenger_details": passengers_berth_info
        }
        return JSONResponse(status_code=200, content = booked_details_response)
    