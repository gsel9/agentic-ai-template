from pydantic import BaseModel


class Query(BaseModel):
    """
    Data model for user message and conversation history.
    """
    item_id: str
    user_id: str
    conv_id: str
    user_input: str