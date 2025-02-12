
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal

### ✅ User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: Optional[Literal["attendee", "organizer", "admin"]] = "attendee"

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: Literal["attendee", "organizer", "admin"]  # ✅ Added role for clarity

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class LoginRequest(BaseModel):
    email: EmailStr  # ✅ Enforce valid email format
    password: str
# class UserLogin(BaseModel):  # ✅ ADDED THIS
#     email: EmailStr
#     password: str

### ✅ Event Schemas
class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    event_date: datetime
    location: str
    max_capacity: int
    registration_deadline: datetime
    category: str
    status: Literal["upcoming", "ongoing", "completed"]

class EventResponse(EventCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_date: Optional[datetime] = None
    location: Optional[str] = None
    max_capacity: Optional[int] = None
    registration_deadline: Optional[datetime] = None
    category: Optional[str] = None
    status: Optional[Literal["upcoming", "ongoing", "completed"]] = None  # ✅ Allow partial updates

### ✅ Registration Schema
class RegistrationResponse(BaseModel):
    id: int
    event_id: int
    user_id: int
    status: Literal["pending", "approved", "rejected"]  # ✅ Use an enum for clarity

    class Config:
        from_attributes = True