from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Message, User
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.utils.auth import decode_access_token

router = APIRouter()
security = HTTPBearer(auto_error=False)

@router.post("/send/{username}")
async def send_message(
    username: str,
    content: str, 
    db: Session = Depends(get_db)
):
    recipient = db.query(User).filter(User.username == username).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    message = Message(content=content, recipient_id=recipient.id)
    db.add(message)
    db.commit()
    db.refresh(message)
    return {"message": "Message sent anonymously!"}

@router.get("/my-messages")
async def get_my_messages(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required")
    token = credentials.credentials
    payload = decode_access_token(token)
    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    messages = db.query(Message).filter(Message.recipient_id == user.id).all()
    return [{"id": m.id, "content": m.content} for m in messages]