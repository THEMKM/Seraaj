from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class Message:
    """A single chat message."""
    sender: str
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Conversation:
    """A conversation between multiple participants."""
    id: str
    participants: List[str] = field(default_factory=list)
    messages: List[Message] = field(default_factory=list)
