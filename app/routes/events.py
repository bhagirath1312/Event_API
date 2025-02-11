# from fastapi import APIRouter, Depends, HTTPException, Request
# from sqlalchemy.orm import Session
# from app import models, schemas, database
# from app.routes.users import get_current_user  # Import user authentication function
# from ..schemas import EventCreate,EventUpdate
# from ..models import Event
# from ..database import get_db
#
# router = APIRouter(tags=["Events"])
#
# # ✅ Create event (User ID should be dynamic)
# @router.post("/events/")
# def create_event(
#     event_data: EventCreate,
#     db: Session = Depends(get_db),
#     user: models.User = Depends(get_current_user)  # ✅ Get logged-in user
# ):
#     event = Event(
#         title=event_data.title,
#         description=event_data.description,
#         event_date=event_data.event_date,  # ✅ Use event_date
#         location=event_data.location,
#         max_capacity=event_data.max_capacity,
#         registration_deadline=event_data.registration_deadline,
#         category=event_data.category,
#         status=event_data.status,
#         user_id=user.id  # ✅ Assign event to logged-in user
#     )
#     db.add(event)
#     db.commit()
#     db.refresh(event)
#     return event
#
# # ✅ Get logged-in user's events
# @router.get("/my-events/")
# def get_user_events(
#     user: models.User = Depends(get_current_user),  # ✅ Ensure authenticated user
#     db: Session = Depends(get_db)
# ):
#     events = db.query(Event).filter(Event.user_id == user.id).all()
#     return {"user": user.email, "events": events}
#
#
# @router.put("/events/{event_id}")
# def update_event(
#     event_id: int,
#     event_data: EventUpdate,
#     db: Session = Depends(get_db),
#     user: models.User = Depends(get_current_user)  # ✅ Ensure authenticated user
# ):
#     event = db.query(Event).filter(Event.id == event_id, Event.user_id == user.id).first()
#
#     if not event:
#         raise HTTPException(status_code=404, detail="Event not found or unauthorized")
#
#     event.title = event_data.title
#     event.description = event_data.description
#     event.event_date = event_data.event_date
#     event.location = event_data.location
#     event.max_capacity = event_data.max_capacity
#     event.registration_deadline = event_data.registration_deadline
#     event.category = event_data.category
#     event.status = event_data.status
#
#     db.commit()
#     db.refresh(event)
#     return {"message": "Event updated successfully", "event": event}
#
# @router.delete("/events/{event_id}")
# def delete_event(
#     event_id: int,
#     db: Session = Depends(get_db),
#     user: models.User = Depends(get_current_user)  # ✅ Ensure authenticated user
# ):
#     event = db.query(Event).filter(Event.id == event_id, Event.user_id == user.id).first()
#
#     if not event:
#         raise HTTPException(status_code=404, detail="Event not found or unauthorized")
#
#     db.delete(event)
#     db.commit()
#     return {"message": "Event deleted successfully"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Event, User
from app.schemas import EventCreate, EventUpdate
from app.database import get_db
from ..auth import get_current_user
from app.dependencies import role_required

router = APIRouter(tags=["Events"])


# Create an event (Only Organizers or Admins)
@router.post("/events/", dependencies=[Depends(role_required(["admin", "organizer"]))])
def create_event(event_data: EventCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    event = Event(
        title=event_data.title,
        description=event_data.description,
        event_date=event_data.event_date,
        location=event_data.location,
        max_capacity=event_data.max_capacity,
        registration_deadline=event_data.registration_deadline,
        category=event_data.category,
        status=event_data.status,
        organizer_id=user.id  # Set the organizer as the creator
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


# Update an event (Only the event creator or Admin)
@router.put("/events/{event_id}", dependencies=[Depends(role_required(["admin", "organizer"]))])
def update_event(event_id: int, event_data: EventUpdate, db: Session = Depends(get_db),
                 user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if user.role != "admin" and event.organizer_id != user.id:
        raise HTTPException(status_code=403, detail="You don't have permission to update this event")

    for key, value in event_data.dict(exclude_unset=True).items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)
    return event


# Delete an event (Only the event creator or Admin)
@router.delete("/events/{event_id}", dependencies=[Depends(role_required(["admin", "organizer"]))])
def delete_event(event_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if user.role != "admin" and event.organizer_id != user.id:
        raise HTTPException(status_code=403, detail="You don't have permission to delete this event")

    db.delete(event)
    db.commit()
    return {"message": "Event deleted successfully"}