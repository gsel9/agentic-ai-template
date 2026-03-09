"""
App router for RAG
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from workflows.rag import run_rag

router = APIRouter()


class Query(BaseModel):
    """
    Data model for user message and conversation history.
    """
    item_id: str
    user_id: str
    conv_id: str
    user_input: str


@router.post("/ask")
def ask_api(query: Query) -> Dict[str, Any]:
    """
    Endpoint to execute chat loop.
    """
    try:
        answer = run_rag(
            query.item_id, query.user_id, query.conv_id, query.user_input
        )
        answer = "This is the answer!!!"
        return {"answer": answer}
    except Exception as exc:
        # log.exception("ask_api failed")  # add logging as needed
        raise HTTPException(status_code=500, detail=str(exc))
