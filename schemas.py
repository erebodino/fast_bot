from pydantic import BaseModel

class Message(BaseModel):
    chatId: int
    messageText: str


class User(BaseModel):
    telegram_id: str

