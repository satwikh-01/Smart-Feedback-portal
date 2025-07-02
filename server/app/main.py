from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# This is a minimal version for debugging purposes.
app = FastAPI(title="Smart Feedback System API - DEBUG")

# Basic CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Root endpoint to check if the server is running."""
    return {"message": "Welcome to the Smart Feedback System API!"}

@app.get("/healthz")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}
