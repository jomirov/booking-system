from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from ..models.seat import SeatCreate
from ..repositories.seatrepository import SeatRepository

router = APIRouter()

@router.post('/api/seats')
async def make_seat(seat: SeatCreate, repo: SeatRepository = Depends(SeatRepository)):
    await repo.create_seat(seat.event_id, seat.row, seat.number, seat.price)
    return JSONResponse({"message": "Seat has been created"}, status_code=201)

@router.get('/api/seats/{event_id}')
async def show_seats_for_event(event_id: int, repo: SeatRepository = Depends(SeatRepository)):
    seats = await repo.get_seats_for_event(event_id)

    return JSONResponse(seats)

@router.get('/api/seats/{event_id}/{id}')
async def show_seat_and_set_status(event_id: int, id: int, repo: SeatRepository = Depends(SeatRepository)):
    seat = await repo.get_seat_for_event_and_update_status_reserved(id, event_id)
    return JSONResponse(seat)

@router.delete('/api/seats/{id}')
async def delete_seat(id: int, repo: SeatRepository = Depends(SeatRepository)):
    await repo.delete_seat(id)
    return JSONResponse({"message": "Seat has been removed"})

@router.put('/api/seats/{id}')
async def update_seat_status(id: int, status: str = Body(), repo: SeatRepository = Depends(SeatRepository)):
    await repo.update_seat_status(id, status)
    return JSONResponse({"message": "Seat status has been updated"})