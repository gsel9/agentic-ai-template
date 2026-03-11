"""
App router for RAG
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from workflows.rag_chat import rag_chat_turn
from routers._datamodels import Query

router = APIRouter()


@router.post("/ask")
def ask_api(query: Query) -> Dict[str, Any]:
    """
    Endpoint to execute chat loop.
    """
    try:
        answer = rag_chat_turn(
            query.item_id, query.user_id, query.conv_id, query.user_input
        )
        return {"answer": answer}
    except Exception as exc:
        # log.exception("ask_api failed")  # add logging as needed
        raise HTTPException(status_code=500, detail=str(exc))
