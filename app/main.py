from fastapi import FastAPI
from app.routes import users , events
from app.database import engine, Base

app = FastAPI(title="Event Management API")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include Routers
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(events.router, prefix="/api/events", tags=["Events"])