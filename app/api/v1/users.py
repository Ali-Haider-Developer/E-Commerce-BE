from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    # TODO: Implement get users logic
    pass

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # TODO: Implement create user logic
    pass

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    # TODO: Implement get user logic
    pass

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    # TODO: Implement update user logic
    pass

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    # TODO: Implement delete user logic
    pass
