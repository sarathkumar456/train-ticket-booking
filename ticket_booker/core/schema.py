from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class AvailableResponse(BaseModel):
    confirmed: int = Field(..., description="Total no of confirmed tickets")
    wl: int = Field(..., description="Total no of waiting list tickets")
    rac: int = Field(..., description="Total no of RAC ticks (2 tickets per berth)")
    
class BookedResponse(AvailableResponse):
    pass
    
class TicketNotAvailableResponse(BaseModel):
    message: str
    
class PassengerResponse(BaseModel):
    name: str = Field(..., example="sarathkumar")
    age: int = Field(..., example=28)
    gender: str = Field(..., example="male")
    berth_type: str = Field(..., example="confirmed")
    berth_no: Optional[str] = Field(None, example="B1-32")

class BookingDetailsResponse(BaseModel):
    booking_id: str = Field(..., example="PNR10211", description="pnr")
    booked_user: str = Field(..., example="johndoe", description="Username of the person who booked the ticket")
    from_location: str = Field(..., example="NDLS", description="Source station name")
    to_location: str = Field(..., example="BCT", description="Destination station name")
    departure_date: datetime = Field(..., example="2025-03-25T10:00:00", description="Date of travel")
    booked_on: datetime = Field(..., example="2025-03-13T15:45:00", description="Date when ticket was booked")
    passenger_details: List[PassengerResponse] = Field(..., description="List of passengers")
    
AvailableExampleResponse = {
        200: {
            "model": AvailableResponse, 
                "description": "Returns response of total berths available for each berth type",
                "content": {
                    "application/json": {
                    "example": {
                        "confirmed": 20,
                        "wl": 10,
                        "rac": 18
                    }
                }
                }
            },
    }

BookedExampleResponse = {
        200: {
            "model": BookedResponse, 
                "description": "Returns response of total berths booked for each berth type",
                "content": {
                    "application/json": {
                    "example": {
                        "confirmed": 63,
                        "wl": 1,
                        "rac": 18
                    }
                }
                }
            },
    }