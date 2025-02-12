from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status, APIRouter
from jose import jwt
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.auth import get_current_user
from app.database import get_db
from app.utils.security import verify_password, hash_password, SECRET_KEY, ALGORITHM
from app.config import settings

router = APIRouter(tags=["Users"])
@router.post("/register", response_model=schemas.UserResponse)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Register a new user with hashed password."""
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_data.password)
    new_user = models.User(
        email=user_data.email,
        full_name=user_data.full_name,
        password_hash=hashed_password,
        role=user_data.role or "attendee"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@router.post("/login")
def login_user(user_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.email).first()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + access_token_expires
    access_token = jwt.encode({"sub": user.email, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES
    }


@router.get("/me", response_model=schemas.UserResponse)
def get_me(user: models.User = Depends(get_current_user)):
    """Returns the details of the currently logged-in user."""
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role
    }



@router.put("/me/update-role")
def update_user_role(new_role: str, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if new_role not in ["attendee", "organizer"]:
        raise HTTPException(status_code=400, detail="Invalid role. Choose 'attendee' or 'organizer'.")
    user.role = new_role
    db.commit()
    db.refresh(user)
    return {"message": f"Role updated successfully to {user.role}"}

@router.get("/your-registered-events")
def get_registered_events(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    registered_events = (
        db.query(models.Event)
        .join(models.Registration)
        .filter(models.Registration.user_id == current_user.id)
        .all()
    )
    return {"user_id": current_user.id, "registered_events": registered_events}