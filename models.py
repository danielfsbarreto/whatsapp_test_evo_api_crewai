from typing import Literal

from pydantic import BaseModel


class WhatsappRequestBody(BaseModel):
    class Config:
        extra = "allow"


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class Conversation(BaseModel):
    id: str
    messages: list[Message]
