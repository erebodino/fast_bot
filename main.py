from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, status
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Annotated, List
import models


class Message(BaseModel):
    chatId: int
    messageText: str

class User(BaseModel):
    telegram_id:str

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/create_user/")
def create_user(user_telegram_id:User, db:db_dependency):
    new_user = models.User(telegram_id = user_telegram_id.telegram_id)
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()  # Es importante hacer rollback para limpiar la sesión de DB
        # Levanta una excepción HTTP con un mensaje adecuado
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The user with  telegram_id {user_telegram_id.telegram_id} already exists."
        )
    db.refresh(new_user)
    return {"user_id": new_user.id, "telegram_id": new_user.telegram_id}


@app.post("/api/v1/message")
def message(message:Message, db:db_dependency):
    user = db.query(models.User).filter(models.User.telegram_id == str(message.chatId)).first()
    if user:
        return {"chat_id":message.chatId, "message":"The rest framework read the --{}--".format(message.messageText)}