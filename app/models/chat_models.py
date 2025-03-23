from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class ChatRequest(BaseModel):

    conversation_id: int = Field(
        ..., description="ID used to associate messages with a conversation"
    )

    chat_history: Optional[List[Message]] = Field(
        None, description="Previous conversation history for context (optional)"
    )


class ChatResponse(BaseModel):
    conversation_id: int
    reply: str  # <-- changed from 'response' to 'reply'
    updated_history: List[Message]
