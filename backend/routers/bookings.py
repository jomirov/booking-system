from fastapi import HTTPException, Depends, Body
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from ..repositories.bookingrepository import BookingRepository
from ..models.booking import BookingCreate

router = APIRouter()

@router.post('/api/bookings')
async def make_booking(booking: BookingCreate, repo: BookingRepository = Depends(BookingRepository)):
    await repo.create_booking(booking.user_id, booking.seat_id)
    return JSONResponse({"message": "Booking has been created"}, status_code=201)

@router.get('/api/bookings')
async def show_all_pending_bookings(repo: BookingRepository = Depends(BookingRepository)):
    bookings = await repo.get_all_pending_bookings()

    return JSONResponse(bookings)

@router.delete('/api/bookings/{id}')
async def delete_booking(id: int, repo: BookingRepository = Depends(BookingRepository)):
    await repo.delete_booking(id)
    return JSONResponse({"message": "Booking has been removed"})

@router.put('/api/bookings/{id}')
async def set_booking_status(id: int, status = Body(), repo: BookingRepository = Depends(BookingRepository)):
    await repo.update_booking_status(id, status)
    return JSONResponse({"message": "Booking status has been updated"})