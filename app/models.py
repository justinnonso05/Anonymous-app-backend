import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)  
    password = Column(String)
    
    messages = relationship("Message", back_populates="recipient") 

class Message(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    content = Column(String)
    recipient_id = Column(String(36), ForeignKey('users.id'), index=True)

    recipient = relationship("User", back_populates="messages")