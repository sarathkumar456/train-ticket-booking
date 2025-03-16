from pydantic import BaseModel

class AvailableResponse(BaseModel):
    confirmed: int 
    wl: int
    rac: int
    
class TicketNotAvailableResponse(BaseModel):
    message: str
    

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