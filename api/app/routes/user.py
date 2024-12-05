from fastapi import APIRouter
from app.models.user import User

router = APIRouter()

@router.get("/users", response_model=list[User])
def get_users():
    return [
        {"id": 1, "username": "user1", "email": "user1@example.com"},
        {"id": 2, "username": "user2", "email": "user2@example.com"},
    ]