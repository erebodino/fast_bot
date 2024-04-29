from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import MONEY, TIMESTAMP
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    telegram_id = Column(Text, unique=True, nullable=False)

class Expense(Base):
    __tablename__ = 'expenses'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    description = Column(Text, nullable=False)
    amount = Column(MONEY, nullable=False)
    category = Column(Text, nullable=False)
    added_at = Column(TIMESTAMP, nullable=False)
