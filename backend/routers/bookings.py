from fastapi import HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.exc import DBAPIError

from ..models.booking import BookingCreate
from ..repositories.bookingrepository import BookingRepository
from ..repositories.seatrepository import SeatRepository

router = APIRouter()

@router.post('/api/bookings')
async def add_booking_and_reserve_seat_and_cancel_other_bookings_of_user(booking: BookingCreate, 
                                       book_repo: BookingRepository = Depends(BookingRepository),
                                       seat_repo: SeatRepository = Depends(SeatRepository)):
    try:
        await seat_repo.update_free_seat_status(booking.seat_id, "RESERVED")
        await book_repo.create_booking(booking.user_id, booking.seat_id)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=e.args[0])
    updated_bookings_seats_id = await book_repo.update_inactive_user_bookings_status_except_one(booking.seat_id, booking.user_id)
    if updated_bookings_seats_id != []:
        await seat_repo.update_many_seats_status(updated_bookings_seats_id, "FREE")

    return JSONResponse({"message": "Booking has been created"}, status_code=201)
# User picks a seat for book (Server checks if there is active booking of user related to current seat ? 
# (YES) Server doesn't create a book log : (NO) Server creates a book log)
@router.get('/api/bookings/active')
async def show_active_booking_of_user(user_id: int = Query(), repo: BookingRepository = Depends(BookingRepository)):
    booking = await repo.get_active_user_booking(user_id)
    return JSONResponse(booking)

@router.put('/api/bookings/expired')
async def make_bookings_expired(book_repo: BookingRepository = Depends(BookingRepository),
                                seat_repo: SeatRepository = Depends(SeatRepository)):
    
    updated_seats_id = await book_repo.update_expired_bookings()
    print("Resetted seats:", updated_seats_id)
    await seat_repo.update_many_seats_status(updated_seats_id, "FREE")
    
    return JSONResponse({"seats_id": updated_seats_id})

@router.put('/api/bookings/book')
async def book_seat(user_id: int = Query(), 
                    book_repo: BookingRepository = Depends(BookingRepository),
                    seat_repo: SeatRepository = Depends(SeatRepository)):
    
    current_booking = await book_repo.get_active_user_booking(user_id)
    if not current_booking:
        raise HTTPException(status_code=404, detail="Couldn't identify current booking")
    
    await book_repo.update_booking_status(current_booking["id"], "PAID")
    await seat_repo.update_seat_status(current_booking["seat_id"], "BOOKED")

    return JSONResponse({"message": "Seat has been booked"})

@router.get('/api/bookings')
async def show_bookings(repo: BookingRepository = Depends(BookingRepository)):
    bookings = await repo.get_bookings()

    return JSONResponse(bookings)