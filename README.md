# In-Platform Messaging Prototype

This project provides a minimal FastAPI backend implementing in-platform messaging between volunteers and organizations.

## Features
- REST endpoints for creating users, conversations, and messages
- Fetching conversation history
- WebSocket endpoint for real-time chat

## Running
Create a virtual environment, install requirements, and run with Uvicorn:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
