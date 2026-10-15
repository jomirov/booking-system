from fastapi import HTTPException, Depends, Body
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from ..models.booking import BookingCreate
from ..repositories.bookingrepository import BookingRepository

router = APIRouter()

@router.post('/api/bookings')
async def add_booking(booking: BookingCreate, repo: BookingRepository = Depends(BookingRepository)):
    try:
        await repo.create_booking(booking.user_id, booking.seat_id)
    except ValueError:
        raise HTTPException(status_code=404)

    return JSONResponse({"message": "Booking has been created"}, status_code=201)

@router.put('/api/bookings/expired')
async def make_bookings_expired(repo: BookingRepository = Depends(BookingRepository)):
    await repo.update_expired_bookings()
    return JSONResponse({"message": "Expired bookings status has been updated"})

@router.put('/api/bookings/{id}')
async def change_booking_status(id: int, status: str = Body(), repo: BookingRepository = Depends(BookingRepository)):
    try:
        await repo.update_booking_status(id, status)
    except ValueError as e:
        if e.args == ('id',):
            raise HTTPException(status_code=404, detail="Booking not found")
        elif e.args == ('status',):
            raise HTTPException(status_code=400, detail="Status value is incorrect")
    return JSONResponse({"message": "Booking status has been updated"})