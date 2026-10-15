from fastapi import HTTPException, Depends, Query, Body
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from ..models.seat import Seat, SeatCreate
from ..repositories.seatrepository import SeatRepository


router = APIRouter()

@router.post('/api/seats')
async def add_seats(event_id: int = Query(), seats: list[SeatCreate] = Body(), repo: SeatRepository = Depends(SeatRepository)):
    try:
        await repo.create_seats(event_id, seats)
    except ValueError as e:
        if e.args == ('seat',):
            raise HTTPException(status_code=400, detail="Seat parameters are incorrect")
        elif e.args == ('event_id',):
            raise HTTPException(status_code=404, detail="Event not found")

    return JSONResponse({"message": "Seat has been created"}, status_code=201)

@router.get('/api/seats/{id}')
async def show_seat(id: int, repo: SeatRepository = Depends(SeatRepository)):
    try:
        seat = await repo.get_seat(id)
    except ValueError as e:
        if e.args == ('id',):
            raise HTTPException(status_code=404)

    return JSONResponse(seat)

@router.get('/api/seats')
async def show_seats_for_event(event_id: int = Query(), repo: SeatRepository = Depends(SeatRepository)):
    try:
        seats = await repo.get_seats_for_event(event_id)
    except ValueError:
        raise HTTPException(status_code=404)
    return JSONResponse(seats)

@router.put('/api/seats/{id}')
async def edit_seat(id: int, new_seat: SeatCreate, repo: SeatRepository = Depends(SeatRepository)):
    try:
        await repo.update_seat(id, new_seat.row, new_seat.number, new_seat.price)
    except ValueError as e:
        if e.args == ('id',):
            raise HTTPException(status_code=404, detail=e)
        elif e.args == ('seat',):
            raise HTTPException(status_code=400, detail=e)

    return JSONResponse({"message": "Seat has been edited"})

@router.delete('/api/seats/{id}')
async def remove_seat(id: int, repo: SeatRepository = Depends(SeatRepository)):
    try:
        await repo.delete_seat(id)
    except ValueError:
        raise HTTPException(status_code=404)
    return JSONResponse({"message": "Seat has been removed"})