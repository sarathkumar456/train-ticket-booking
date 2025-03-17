from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date
from core.config import IST

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

class PassengerBaseInfo(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, example="Sarathkumar Shrinivasa")
    age: int = Field(..., ge=1, le=120, example=27)
    gender: str = Field(..., example="Male")
    
class PassengerRequestBody(PassengerBaseInfo):
    children: List[PassengerBaseInfo] = Field([], description="List of children info in dictionary with fields name, age, gender")
    
    @validator("gender")
    def validate_gender(cls, value):
        if value.lower() in ["male", "female", "others"]:
            return value.lower()
        else:
            raise ValueError("Only either one of male, female or others is allowed")
        
class BookingRequestBody(BaseModel):
    booked_user: str = Field(..., example="johndoe", description="Username of the person who booked the ticket")
    source: str = Field(..., min_length=2, max_length=5, example="CMBT", description="Source station code")
    destination: str = Field(..., min_length=2, max_length=5, example="MAS", description="Destination station code")
    travel_date: datetime = Field(..., example="2024-03-18T05:30:00", description="train departure datetime")
    passenger_details: List[PassengerRequestBody]

    @validator("travel_date")
    def validate_travel_date(cls, value):
        value = datetime.fromisoformat(value)
        if value <= datetime.now(IST):
            raise ValueError("Travel date must be in the future")
        return value

    @validator("destination")
    def validate_source_dest(cls, dest, values):
        if "source" in values and values["source"] == dest:
            raise ValueError("Source and destination cannot be the same")
        return dest

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