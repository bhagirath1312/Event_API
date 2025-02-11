from fastapi import Depends, HTTPException,status
from jose import jwt, JWTError
from app.database import get_db
from app.models import User
from sqlalchemy.orm import Session
from .auth import get_current_user
SECRET_KEY = "4f8c3b8e72a1dcb57f9ac27492d8b1d3bfa5e324f1c6789da2b3f7c6d5e4a1f2"
ALGORITHM = "HS256"

def role_required(required_roles: list):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden: Insufficient permissions",
            )
        return user
    return role_checker