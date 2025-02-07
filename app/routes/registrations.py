from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter(tags=["Registrations"])


@router.post("/{event_id}/register")
def register_for_event(event_id: int, user_id: int, db: Session = Depends(database.get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.max_capacity and db.query(models.Registration).filter(
            models.Registration.event_id == event_id).count() >= event.max_capacity:
        raise HTTPException(status_code=400, detail="Event is full")

    existing_registration = db.query(models.Registration).filter(
        models.Registration.event_id == event_id, models.Registration.user_id == user_id).first()

    if existing_registration:
        raise HTTPException(status_code=400, detail="Already registered for this event")

    registration = models.Registration(event_id=event_id, user_id=user_id, status="registered")
    db.add(registration)
    db.commit()
    return {"message": "Registration successful"}


@router.get("/{event_id}/registrations")
def get_event_registrations(event_id: int, db: Session = Depends(database.get_db)):
    registrations = db.query(models.Registration).filter(models.Registration.event_id == event_id).all()
    return registrations


@router.delete("/{event_id}/registrations/{user_id}")
def cancel_registration(event_id: int, user_id: int, db: Session = Depends(database.get_db)):
    registration = db.query(models.Registration).filter(
        models.Registration.event_id == event_id, models.Registration.user_id == user_id).first()

    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    db.delete(registration)
    db.commit()
    return {"message": "Registration cancelled"}