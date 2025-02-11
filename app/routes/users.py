# from datetime import timedelta, datetime
# from fastapi import Depends, HTTPException, status, APIRouter
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import jwt, JWTError
# from sqlalchemy.orm import Session
# from app import database, models, schemas
# from app.utils.security import verify_password, hash_password
# from app.config import settings
#
# router = APIRouter(tags=["Users"])
#
# # OAuth2 authentication setup
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")
#
#
# @router.post("/register", response_model=schemas.UserResponse)
# def register_user(user_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
#     """Registers a new user after checking if the email is already registered."""
#     existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#
#     hashed_password = hash_password(user_data.password)
#     new_user = models.User(
#         email=user_data.email,
#         password_hash=hashed_password,
#         full_name=user_data.full_name,
#         role="attendee"
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user
#
#
# @router.post("/login")
# def login_user(user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
#     """Logs in a user by verifying credentials and returning a JWT token."""
#     user = db.query(models.User).filter(models.User.email == user_data.username).first()
#
#     if not user or not verify_password(user_data.password, user.password_hash):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
#
#     # Generate JWT Token
#     access_token_expires = timedelta(minutes=30)
#     expire = datetime.utcnow() + access_token_expires
#     access_token = jwt.encode({"sub": user.email, "exp": expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
#
#     return {"access_token": access_token, "token_type": "bearer"}
#
#
# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
#     """Extracts and verifies the user from the provided JWT token."""
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         print(f"🔹 Received Token: {token}")  # Debugging
#
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         user_email: str = payload.get("sub")
#
#         if user_email is None:
#             print("🔴 Invalid Token (sub missing)")
#             raise credentials_exception
#
#         user = db.query(models.User).filter(models.User.email == user_email).first()
#
#         if user is None:
#             print("🔴 User not found for email:", user_email)
#             raise credentials_exception
#
#         return user
#     except JWTError as e:
#         print(f"🔴 JWTError: {str(e)}")
#         raise credentials_exception
#
#
# @router.get("/me", response_model=schemas.UserResponse)
# def get_me(current_user: schemas.UserResponse = Depends(get_current_user)):
#     """Returns the details of the currently logged-in user."""
#     return current_user




from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, func
from app import database, models, schemas
from app.database import get_db
from app.utils.security import verify_password, hash_password
from app.config import settings
from app.database import get_db
router = APIRouter(tags=["Users"])

# OAuth2 authentication setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


@router.post("/register", response_model=schemas.UserResponse)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Registers a new user after checking if the email is already registered."""
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_data.password)
    new_user = models.User(
        email=user_data.email,
        full_name=user_data.full_name,  # ✅ Ensure this is being assigned
        password_hash=hash_password(user_data.password),
        role=Column(String, default="attendee", server_default="attendee", nullable=False)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login_user(user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """Logs in a user by verifying credentials and returning a JWT token."""
    user = db.query(models.User).filter(models.User.email == user_data.username).first()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Generate JWT Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + access_token_expires
    access_token = jwt.encode({"sub": user.email, "exp": expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """Extracts and verifies the user from the provided JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_email: str = payload.get("sub")

        if user_email is None:
            raise credentials_exception

        user = db.query(models.User).filter(models.User.email == user_email).first()

        if user is None:
            raise credentials_exception

        return user  # ✅ Now returns SQLAlchemy User object instead of dict
    except JWTError:
        raise credentials_exception


# @router.get("/me", response_model=schemas.UserResponse)
# def get_me(current_user: models.User = Depends(get_current_user)):
#     """Returns the details of the currently logged-in user."""
#     return schemas.UserResponse(id=current_user.id, email=current_user.email)

@router.get("/me")
def get_me(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
    }


@router.put("/me/update-role")
def update_user_role(new_role: str, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if new_role not in ["attendee", "organizer"]:
        raise HTTPException(status_code=400, detail="Invalid role. Choose 'attendee' or 'organizer'.")

    user.role = new_role
    db.commit()
    db.refresh(user)

    return {
        "message": f"Role updated successfully to {user.role}",
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role
    }