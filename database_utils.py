
import models
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

def get_user_by_telegram_id(db:sessionmaker, telegram_id:str):
    """Function to retrieve the user who sent the message, could be None if the user doesn't exist.

    Args:
        db (sessionmaker): db connection
        telegram_id (str): telegram id passed from front end
    """
    return db.query(models.User).filter(models.User.telegram_id == str(telegram_id)).first()

def add_expense_to_db(db:sessionmaker, user_id:str, expense_data:dict):
    """
    Function to persist a expense into the database. All the data must be available in the expense_data dict,
    if some value is missing or the dict is empty, it will not trigger the record.

    Args:
        db (sessionmaker): db connection
        user_id (str): user_id from the User model.
        expense_data (dict): Dict with the -expense_name-, -category-, and -amount- keys.
    """
    expense_name = expense_data.get("expense_name",None)
    category = expense_data.get("category",None)
    amount = expense_data.get("amount",None)

    if expense_name and category and amount:
        new_expense = models.Expense(
            user_id=user_id,
            description=expense_name,
            amount=amount,
            category=category,
            added_at=datetime.datetime.now(),
        )
        db.add(new_expense)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()