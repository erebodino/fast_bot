
from fastapi import FastAPI, Depends, HTTPException, status
from database import engine, db_dependency
from sqlalchemy.exc import IntegrityError
from chain_conection import BotAI
from anthropic import InternalServerError
from schemas import User, Message
from database_utils import get_user_by_telegram_id, add_expense_to_db
import models


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@app.post("/create_user/")
def create_user(user_telegram_id: User, db: db_dependency):
    new_user = models.User(telegram_id=user_telegram_id.telegram_id)
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback() 
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The user with  telegram_id {user_telegram_id.telegram_id} already exists.",
        )
    db.refresh(new_user)
    return {"user_id": new_user.id, "telegram_id": new_user.telegram_id}


@app.post("/api/v1/message")
async def message(message: Message, db: db_dependency):
    response = {}
    user = get_user_by_telegram_id(db, message.chatId)    
    if not user:
        return {"chat_id": message.chatId, "message": response}
    else:
        bot = BotAI()
        chain = bot.create_chain()
        try:
            response = await chain.ainvoke({"query": message.messageText})
            add_expense_to_db(db, user_id=user.id, expense_data = response)
        except InternalServerError: #Due to overload from Anthropic
            response = {'error_msg':'Cannot process your request, please try again later.'}  
        return {"chat_id": message.chatId, "message": response}
