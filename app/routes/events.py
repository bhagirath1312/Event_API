from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.routes.users import get_current_user
from ..schemas import EventCreate
from ..models import Event
from ..database import get_db
router = APIRouter(tags=["Events"])

@router.post("/events/")
def create_event(event_data: EventCreate, db: Session = Depends(get_db)):
    event = Event(
        title=event_data.title,
        description=event_data.description,
        event_date=event_data.event_date,  # ✅ Use event_date
        location=event_data.location,
        max_capacity=event_data.max_capacity,
        registration_deadline=event_data.registration_deadline,
        category=event_data.category,
        status=event_data.status,
        user_id=1  # Replace with actual user ID
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event