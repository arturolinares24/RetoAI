from app import app  # Importing the FastAPI app instance correctly assuming it's defined in app/__init__.py
import uvicorn


def run_server():
    """
    Run the FastAPI server using uvicorn.
    """
    # Run the server with uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    # Run the server when this script is executed directly
    run_server()
