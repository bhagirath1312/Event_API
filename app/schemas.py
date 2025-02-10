from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    access_token: str
    token_type: str



class EventCreate(BaseModel):
    title: str
    description: str
    event_date: datetime  # ✅ Use event_date
    location: str
    max_capacity: int
    registration_deadline: datetime
    category: str
    status: str

class EventResponse(EventCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True