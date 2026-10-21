from fastapi import HTTPException, Depends, Body
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

from ..repositories.eventrepository import EventRepository
from ..models.event import EventCreate

router = APIRouter()

@router.post('/api/events')
async def add_event(event: EventCreate, repo: EventRepository = Depends(EventRepository)):
    await repo.create_event(event.title, event.date, event.location)

    return JSONResponse({"message": "Event has been created"}, status_code=201)

@router.get('/api/events')
async def show_active_events(repo: EventRepository = Depends(EventRepository)):
    events = await repo.get_active_events()
    return JSONResponse(events)

@router.get('/api/events/{id}')
async def show_event(id: int, repo: EventRepository = Depends(EventRepository)):
    try:
        event = await repo.get_event(id)
    except ValueError:
        raise HTTPException(status_code=404)

    return JSONResponse(event)

@router.delete('/api/events/{id}')
async def remove_event(id: int, repo: EventRepository = Depends(EventRepository)):
    try:
        await repo.delete_event(id)
    except ValueError:
        raise HTTPException(status_code=404)

    return JSONResponse({"message": "Event has been removed"})