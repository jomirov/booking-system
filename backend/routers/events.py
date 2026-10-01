from fastapi import Depends, HTTPException, Body
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from ..models.event import EventCreate
from ..repositories.eventrepository import EventRepository
from ..dependencies import validate_date

router = APIRouter()

@router.post('/api/events')
async def make_event(event: EventCreate = Body(), repo: EventRepository = Depends(EventRepository)):
    if not validate_date(event.date):
        raise HTTPException(status_code=400, detail="Date is invalid")
    await repo.create_event(event.title, event.date)
    return JSONResponse({"message": "Event has been created"}, status_code=201)

@router.get('/api/events')
async def show_all_events(repo: EventRepository = Depends(EventRepository)):
    events = await repo.get_events()
    return JSONResponse(events)

@router.delete('/api/events/{id}')
async def delete_event(id: int, repo: EventRepository = Depends(EventRepository)):
    await repo.delete_event(id)
    return JSONResponse({"message": "Event has been removed"})