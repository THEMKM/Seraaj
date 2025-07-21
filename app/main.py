from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from sqlmodel import select
from typing import List
from app.database import engine, init_db, get_session
from app.models import User, Conversation, Message
from app.schemas import UserCreate, ConversationCreate, MessageCreate, MessageRead

app = FastAPI()

init_db()

@app.post("/users", response_model=User)
def create_user(user: UserCreate, session=Depends(get_session)):
    db_user = User.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.post("/conversations", response_model=Conversation)
def create_conversation(conv: ConversationCreate, session=Depends(get_session)):
    conversation = Conversation(**conv.dict())
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation

@app.post("/conversations/{conversation_id}/messages", response_model=MessageRead)
def send_message(conversation_id: int, msg: MessageCreate, session=Depends(get_session)):
    message = Message(conversation_id=conversation_id, **msg.dict())
    session.add(message)
    session.commit()
    session.refresh(message)
    return message

@app.get("/conversations/{conversation_id}/messages", response_model=List[MessageRead])
def get_messages(conversation_id: int, session=Depends(get_session)):
    messages = session.exec(select(Message).where(Message.conversation_id==conversation_id).order_by(Message.timestamp)).all()
    return messages

# In-memory connection management
active_connections = {}

@app.websocket("/ws/chat/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: int):
    await websocket.accept()
    if conversation_id not in active_connections:
        active_connections[conversation_id] = []
    active_connections[conversation_id].append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # echo to all connections in conversation
            for connection in active_connections.get(conversation_id, []):
                await connection.send_text(data)
    except WebSocketDisconnect:
        active_connections[conversation_id].remove(websocket)
