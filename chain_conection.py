from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional
from langchain_core.messages import AIMessage
from langchain_anthropic import ChatAnthropic
import json
import os

LLM_API_KEY = os.environ.get("LLM_API_KEY")

class Expense(BaseModel):
    """
    Information about the expense performed by an user.

    Is used as a model for the LLM so it has a way to understand better the output required for the task.
    """

    expense_name: Optional[str] = Field(default=None, description="The expense itself.")
    category: Optional[str] = Field(
        default=None,
        description="The category on which the expense belongs. Can be one of the following: Housing, Transportation, Food, Utilities, Insurance,"
        "Medical/Healthcare, Savings, Debt, Education, Entertainment, and Other.",
    )
    amount: Optional[float] = Field(
        default=None,
        description="The amount of money spend on the expense, it can be given by the user in correct way as  40 USD, 23.33 ARS or another currency or with a slang (Bucks, Pesos, etc)",
    )


def extract_json(message: AIMessage) -> dict:
    """
    Extract and return the data for the expense in the case that exists. Return empty dict otherwise.

    Args:
        message (AIMessage): Message returned by the AI
    """
    text = message.content
    try:
        return json.loads(text)
    except Exception:
        return {}


class BotAI:
    """
    Class to create a Bot and perform a LLM consult. The prompt is pre loaded to be able to perform the consult.
    """
    def __init__(self):
        self.llm = ChatOllama(model="llama3", temperature=0)
        # self.llm = ChatAnthropic(model="claude-3-opus-20240229", api_key=LLM_API_KEY, temperature=0)

    def create_prompt(self) -> ChatPromptTemplate:
        """
        Method to create the prompt with the pre-loaded suggestions for the model.

        Returns:
            ChatPromptTemplate: ChatPromtTemplate with the sugestions to the model on how manage the information passed.
        """
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
        """
        Create a chain with the model, the promt and the extract function.
        Set a retry policy due to problems with invoke and ainvoke.
        """
        self.chain = self.create_prompt() | self.llm | extract_json
        self.chain = self.chain.with_retry()
        return self.chain
