from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Event, User
from app.schemas import EventCreate, EventUpdate
from app.database import get_db
from .. import database, auth
from app.dependencies import role_required
import  app.models as models
from app.auth import get_current_user
router = APIRouter(tags=["Events"])


# Create an event (Only Organizers or Admins)
@router.post("/events/")
def create_event(
    event_data: EventCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)  # ✅ Correct dependency
):
    print("DEBUG: Current user type ->", type(current_user))  # Debugging
    print("DEBUG: Current user data ->", current_user)  # Debugging

    if not isinstance(current_user, models.User):  # Extra safety check
        raise HTTPException(status_code=500, detail="Invalid user data received, expected User model but got another type")

    if current_user.role != "organizer":
        raise HTTPException(status_code=403, detail="Only organizers can create events")

    event = models.Event(
        title=event_data.title,
        description=event_data.description,
        event_date=event_data.event_date,
        location=event_data.location,
        max_capacity=event_data.max_capacity,
        registration_deadline=event_data.registration_deadline,
        category=event_data.category,
        status=event_data.status,
        organizer_id=current_user.id
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

@router.post("/{event_id}/register")
def register_event(event_id: int, db: Session = Depends(database.get_db), user: models.User = Depends(auth.get_current_user)):
    """Registers an attendee for an event or adds them to a waiting list if full."""

    if user.role != "attendee":
        raise HTTPException(status_code=403, detail="Only attendees can register for events")

    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Count current registrations
    registered_count = db.query(models.Registration).filter(models.Registration.event_id == event_id).count()

    # Check if user is already registered
    existing_registration = db.query(models.Registration).filter_by(user_id=user.id, event_id=event_id).first()
    if existing_registration:
        raise HTTPException(status_code=400, detail="Already registered for this event")

    if registered_count < event.max_capacity:
        # ✅ Register user normally
        registration = models.Registration(user_id=user.id, event_id=event_id, status="registered")
        db.add(registration)
        message = "Successfully registered for the event"
    else:
        # 🔹 Add user to waiting list
        waiting_entry = models.WaitingList(user_id=user.id, event_id=event_id)
        db.add(waiting_entry)
        message = "Event is full. You have been added to the waiting list."

    db.commit()
    return {"message": message}

@router.post("/{event_id}/cancel")
def cancel_registration(event_id: int, db: Session = Depends(database.get_db), user: models.User = Depends(auth.get_current_user)):
    """Allows users to cancel their event registration, and moves the first person from the waiting list if available."""

    registration = db.query(models.Registration).filter_by(user_id=user.id, event_id=event_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="You are not registered for this event")

    db.delete(registration)
    db.commit()

    # 🔄 Check if there's anyone on the waiting list
    next_waiting = db.query(models.WaitingList).filter(models.WaitingList.event_id == event_id).order_by(models.WaitingList.id).first()

    if next_waiting:
        # Move waiting list user to registered attendees
        new_registration = models.Registration(user_id=next_waiting.user_id, event_id=event_id, status="registered")
        db.add(new_registration)
        db.delete(next_waiting)  # Remove from waiting list
        db.commit()
        return {"message": "Registration canceled. A user from the waiting list has been registered."}

    return {"message": "Registration canceled successfully."}
@router.get("/events", tags=["Events"])
def get_all_events(db: Session = Depends(get_db)):
    """Fetch all available events from all organizers."""

    events = db.query(models.Event).all()
    return {"total_events": len(events), "events": events}
