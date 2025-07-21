from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str

class ConversationCreate(BaseModel):
    volunteer_id: int
    organization_id: int

class MessageCreate(BaseModel):
    sender_id: int
    content: str

class MessageRead(BaseModel):
    id: int
    conversation_id: int
    sender_id: int
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True
