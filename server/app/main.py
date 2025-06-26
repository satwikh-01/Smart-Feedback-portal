from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, teams, feedback # Import the new feedback router
from app.models import relationships # Ensure relationships are configured

app = FastAPI(title="Smart Feedback System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Smart Feedback System API!"}

# Add routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(teams.router, prefix="/api/v1/teams", tags=["Teams"])
app.include_router(feedback.router, prefix="/api/v1/feedback", tags=["Feedback"])