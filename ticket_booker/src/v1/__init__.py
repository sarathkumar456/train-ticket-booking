from fastapi import APIRouter
from .available import router as available_router
from .booked import router as booked_router
from .book_ticket import router as book_ticket_router

router = APIRouter(prefix='/api/v1')

router.include_router(available_router, tags=['Available Tickets Api'])
router.include_router(booked_router, tags=["Booked Tickets Api"])
router.include_router(book_ticket_router, tags=["Book Ticket Api"])

