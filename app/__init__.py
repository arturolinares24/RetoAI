from fastapi import FastAPI
from .routes.routes import router  # Import the router from the routes package
from .config import DIRECTORY
from .utils import create_directory

# Initialize FastAPI app here
app = FastAPI(title="Reto AI", version="1.0")


# Define startup event handler to create directory on app startup
@app.on_event("startup")
def startup_event():
    """
    Event handler to create directory on application startup.
    """
    create_directory(DIRECTORY)


# Include router in the FastAPI app
app.include_router(router)
