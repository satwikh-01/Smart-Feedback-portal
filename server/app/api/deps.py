from typing import Generator
from app.db.session import SessionLocal

def get_db() -> Generator:
    """
    A dependency that provides a database session for each request.
    It ensures the database session is always closed after the request,
    even if an error occurs.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
