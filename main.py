from pydantic import BaseModel

from fastapi import FastAPI


class Message(BaseModel):
    chatId: int
    messageText: str

app = FastAPI()


@app.post("/api/v1/message")
def message(message:Message):
    return {"chat_id":message.chatId, "message":"The rest framework read the --{}--".format(message.messageText)}