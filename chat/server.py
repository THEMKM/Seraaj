from datetime import datetime
from typing import Dict, List
from uuid import uuid4

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from .models import Conversation, Message

app = FastAPI()

# Simple in-memory stores. These are not persistent and are meant for the prototype.
conversations: Dict[str, Conversation] = {}
websocket_connections: Dict[str, List[WebSocket]] = {}


class CreateConversationRequest(BaseModel):
    participants: List[str]


class SendMessageRequest(BaseModel):
    sender: str
    content: str


@app.post("/conversations")
async def create_conversation(req: CreateConversationRequest):
    conv_id = str(uuid4())
    conversation = Conversation(id=conv_id, participants=req.participants)
    conversations[conv_id] = conversation
    websocket_connections[conv_id] = []
    return {"id": conv_id}


@app.get("/conversations/{conv_id}")
async def get_conversation(conv_id: str):
    conversation = conversations.get(conv_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {
        "id": conversation.id,
        "participants": conversation.participants,
        "messages": [
            {
                "sender": m.sender,
                "content": m.content,
                "timestamp": m.timestamp.isoformat(),
            }
            for m in conversation.messages
        ],
    }


@app.post("/conversations/{conv_id}/messages")
async def send_message(conv_id: str, req: SendMessageRequest):
    conversation = conversations.get(conv_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    message = Message(sender=req.sender, content=req.content)
    conversation.messages.append(message)

    for ws in list(websocket_connections.get(conv_id, [])):
        try:
            await ws.send_json(
                {
                    "sender": message.sender,
                    "content": message.content,
                    "timestamp": message.timestamp.isoformat(),
                }
            )
        except WebSocketDisconnect:
            websocket_connections[conv_id].remove(ws)
    return {"status": "sent"}


@app.websocket("/ws/chat/{conv_id}")
async def chat_ws(websocket: WebSocket, conv_id: str):
    await websocket.accept()
    if conv_id not in conversations:
        await websocket.close(code=1008)
        return
    websocket_connections.setdefault(conv_id, []).append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = Message(sender="anonymous", content=data, timestamp=datetime.utcnow())
            conversations[conv_id].messages.append(message)
            for ws in list(websocket_connections[conv_id]):
                try:
                    await ws.send_json(
                        {
                            "sender": message.sender,
                            "content": message.content,
                            "timestamp": message.timestamp.isoformat(),
                        }
                    )
                except WebSocketDisconnect:
                    websocket_connections[conv_id].remove(ws)
    except WebSocketDisconnect:
        websocket_connections[conv_id].remove(websocket)
