from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="attendee", nullable=False)
    registrations = relationship("Registration", back_populates="user", cascade="all, delete")
    events = relationship("Event", back_populates="creator")


class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), default="registered")  # Options: registered, waitlisted, cancelled
    registration_date = Column(DateTime, default=func.now())  # Auto timestamp
    attendance_status = Column(Boolean, default=False)  # True if attended, False otherwise

    # Relationships (optional, for ORM usage)
    event = relationship("Event", back_populates="registrations")
    user = relationship("User", back_populates="registrations")
class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    event_date = Column(DateTime, nullable=False)  # ✅ Use event_date
    location = Column(String, nullable=False)
    max_capacity = Column(Integer, nullable=False)
    registration_deadline = Column(DateTime, nullable=False)
    category = Column(String, nullable=False)
    status = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    registrations = relationship("Registration", back_populates="event", cascade="all, delete")
    creator = relationship("User", back_populates="events")