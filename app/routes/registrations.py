import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app import models, database

from app.auth import get_current_user
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Registrations"])


@router.post("/events/{event_id}/register")
def register_for_event(
        event_id: int,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "attendee":
        raise HTTPException(status_code=403, detail="Only attendees can register for events")

    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.organizer_id == current_user.id:
        raise HTTPException(status_code=403, detail="You cannot register for your own event")

    registered_count = db.query(func.count(models.Registration.id)).filter(
        models.Registration.event_id == event_id
    ).scalar()

    if registered_count >= event.max_capacity:
        raise HTTPException(status_code=400, detail="Event is full. Please join the waitlist.")

    existing_registration = db.query(models.Registration).filter(
        models.Registration.user_id == current_user.id,
        models.Registration.event_id == event_id
    ).first()
    if existing_registration:
        raise HTTPException(status_code=400, detail="You are already registered for this event")

    registration = models.Registration(user_id=current_user.id, event_id=event_id, status="registered")
    db.add(registration)
    db.commit()
    db.refresh(registration)

    logger.info(f"User {current_user.id} registered for event {event_id}")
    return {"message": "Successfully registered for the event", "event_id": event_id}


@router.post("/events/{event_id}/admin-register")
def admin_register_for_event(event_id: int, user_id: int, db: Session = Depends(database.get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    registered_count = db.query(func.count(models.Registration.id)).filter(
        models.Registration.event_id == event_id
    ).scalar()

    if registered_count >= event.max_capacity:
        raise HTTPException(status_code=400, detail="Event is full")

    existing_registration = db.query(models.Registration).filter(
        models.Registration.event_id == event_id,
        models.Registration.user_id == user_id
    ).first()
    if existing_registration:
        raise HTTPException(status_code=400, detail="User already registered")

    registration = models.Registration(event_id=event_id, user_id=user_id, status="registered")
    db.add(registration)
    db.commit()

    logger.info(f"Admin registered user {user_id} for event {event_id}")
    return {"message": "Admin successfully registered user for event"}


@router.delete("/events/{event_id}/registrations/{user_id}")
def cancel_registration(event_id: int, user_id: int, db: Session = Depends(database.get_db)):
    registration = db.query(models.Registration).filter(
        models.Registration.event_id == event_id,
        models.Registration.user_id == user_id
    ).first()

    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    db.delete(registration)
    db.commit()

    logger.info(f"User {user_id} canceled registration for event {event_id}")
    return {"message": "Registration cancelled successfully"}