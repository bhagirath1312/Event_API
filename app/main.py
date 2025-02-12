from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.routes import users, events, registrations
from app.database import engine, Base
app = FastAPI(title="Event Management API")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Event Management API",
        version="1.0.0",
        description="API for managing events and registrations",
        routes=app.routes,
    )

    # 🔹 Define Security Scheme (adds the "Authorize" button back)
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # 🔹 Apply Security Globally (so "Authorize" button appears but is not required for all endpoints)
    openapi_schema["security"] = [{"BearerAuth": []}]

    # 🔹 Remove "authorization" from individual paths
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if "parameters" in openapi_schema["paths"][path][method]:
                openapi_schema["paths"][path][method]["parameters"] = [
                    param for param in openapi_schema["paths"][path][method]["parameters"]
                    if param["name"] != "authorization"
                ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Create database tables
Base.metadata.create_all(bind=engine)

# Include Routers
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(events.router, prefix="/api/events", tags=["Events"])
app.include_router(registrations.router, prefix="/api")


