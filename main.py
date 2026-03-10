"""
App entry point.
"""
from fastapi import FastAPI
from routers import rag


app = FastAPI()
app.include_router(rag.router)
