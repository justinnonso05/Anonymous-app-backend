from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin
from app.utils.auth import create_access_token, hash_password, verify_password
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()


@router.post("/register/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "email": new_user.email, "username": new_user.username}

@router.post("/login/")
async def authenticate_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": db_user.username})
    return {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
            "access_token": access_token,
            "token_type": "bearer"
        }