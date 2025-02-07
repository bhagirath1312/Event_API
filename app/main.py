from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from app.database import engine, Base
from app.routes import users, events, registrations
# from app.auth import create_access_token
from app.auth import get_current_user
# Initialize FastAPI app
app = FastAPI(title="Event Management API")

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Authentication scheme for Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Protected route for testing authentication
@app.get("/protected-route")
def protected_route(token: str = Depends(oauth2_scheme)):
    return {"message": "You are authenticated!"}

# Include all API routes
app.include_router(users.router, prefix="/api/users")
app.include_router(events.router, prefix="/api/events")
app.include_router(registrations.router, prefix="/api/registrations")

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Event Management API"}


@app.get("/users/me")
def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}