
from fastapi import FastAPI, Depends, HTTPException, status
from database import engine, db_dependency
from sqlalchemy.exc import IntegrityError
from chain_conection import BotAI
from anthropic import InternalServerError
from schemas import User, Message
from database_utils import get_user_by_telegram_id, add_expense_to_db
from helpers import check_response
import models


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@app.post("/register_user/")
def create_user(user_telegram_id: User, db: db_dependency):
    response = {}
    new_user = models.User(telegram_id=user_telegram_id.telegram_id)
    db.add(new_user)
    try:
        db.commit()
        response['message'] = "You 've been successfully registered."
    except IntegrityError:
        db.rollback()
        response['message'] = "You are alredy registered."
    return response


@app.post("/message/")
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
            safe_response = check_response(response)
            if safe_response:
                add_expense_to_db(db, user_id=user.id, expense_data = response)
            else:
                response = {}
        except InternalServerError: #Due to overload from Anthropic
            response = {'error_msg':'Cannot process your request, please try again later.'}
        return {"chat_id": message.chatId, "message": response}
