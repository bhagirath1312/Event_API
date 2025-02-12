from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Header
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app import models, schemas, database
from app.utils.security import verify_password, hash_password, SECRET_KEY, ALGORITHM
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# @router.post("/register", response_model=schemas.UserResponse)
# def register_user(user_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
#     """Register a new user with hashed password."""
#     existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#
#     hashed_password = hash_password(user_data.password)
#     new_user = models.User(
#         email=user_data.email,
#         full_name=user_data.full_name,
#         password_hash=hashed_password,
#         role=user_data.role or "attendee"
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user
# #
# @router.post("/login", response_model=schemas.Token)
# def login_user(user_data: schemas.LoginRequest, db: Session = Depends(database.get_db)):
#     """Authenticate user and return JWT token."""
#     user = db.query(models.User).filter(models.User.email == user_data.email).first()
#     if not user or not verify_password(user_data.password, user.password_hash):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
#
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     expire = datetime.utcnow() + access_token_expires
#     access_token = jwt.encode({"sub": user.email, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
#
#     return {"access_token": access_token, "token_type": "bearer", "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES}
#
#
def get_current_user(db: Session = Depends(database.get_db), authorization: str = Header(None)):
    """Authenticate user using JWT token from the Authorization header."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not authorization or not authorization.startswith("Bearer "):
        raise credentials_exception

    token = authorization.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise credentials_exception

        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            raise credentials_exception

        return user
    except JWTError:
        raise credentials_exception

# @router.get("/me", response_model=schemas.UserResponse)
# def get_me(user: models.User = Depends(get_current_user)):
#     """Returns the details of the currently logged-in user."""
#     return {
#         "id": user.id,
#         "email": user.email,
#         "full_name": user.full_name,
#         "role": user.role
#     }
