from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, teams, feedback, notifications, ai, users

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

@app.get("/healthz", tags=["Health Check"])
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}

# Add the new users router to the application
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(teams.router, prefix="/api/v1/teams", tags=["Teams"])
app.include_router(feedback.router, prefix="/api/v1/feedback", tags=["Feedback"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["Notifications"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["AI"])
