from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Smart Feedback System API")

# Configure CORS (Cross-Origin Resource Sharing)
# This allows frontend (running on a different domain) to communicate with the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, we'll restrict this to frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# A simple root endpoint to check if the API is running
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Smart Feedback System API!"}