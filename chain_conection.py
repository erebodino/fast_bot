from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional
from langchain_core.messages import AIMessage
import json

class Expense(BaseModel):
    """
    Information about the expense performed by an user.
    """
    expense_name: Optional[str] = Field(default=None, description="The expense itself.")
    category: Optional[str] = Field(
        default=None, description="The category on which the expense belongs. Can be one of the following: Housing, Transportation, Food, Utilities, Insurance," \
                                                "Medical/Healthcare, Savings, Debt, Education, Entertainment, and Other."
    )
    amount: Optional[float] = Field(
        default=None, description="The amount of money spend on the expense, it can be given by the user in correct way as  40 USD, 23.33 ARS or another currency or with a slang (Bucks, Pesos, etc)"
    )

def extract_json(message: AIMessage) -> dict:
    """
    Extract and return the data for the expense in that exists. Return empty dict otherwise.

    Args:
        message (AIMessage): Message returned by the AI

    """
    text = message.content
    try:
        return json.loads(text)
    except Exception:
        return {}

class BotAI:
    def __init__(self):
        self.llm = ChatOllama(model="llama3", temperature=0)
    
    def create_prompt(self):
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Output your answer as JSON that"
                    "matches the given schema: {schema}. Return only the fields expense_name, category and amount, no other field like title or properties."
                    "Given an user text, try to identify expense details and extract them, and with that data fill the response."
                    "Only return the fields in the schema and don't add any comentary in the response."
                    "The category returned must be one of following [Housing, Transportation, Food, Utilities, Insurance,Medical/Healthcare, Savings, Debt, Education, Entertainment] or 'Other' otherwise."
                    "The answer with the fields in the schema should be at last.",
                ),
                ("human", "{query}"),
            ]
            ).partial(schema=Expense.schema())
        return self.prompt

    def create_chain(self):
        self.chain = self.create_prompt() | self.llm | extract_json
        self.chain = self.chain.with_retry()
        return self.chain

    
