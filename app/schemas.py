from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str

class EventCreate(BaseModel):
    title: str
    description: Optional[str]
    event_date: datetime
    location: Optional[str]
    max_capacity: Optional[int]
    registration_deadline: Optional[datetime]
    category: Optional[str]
    status: Optional[str]

class RegistrationCreate(BaseModel):
    event_id: int
    status: Optional[str]

