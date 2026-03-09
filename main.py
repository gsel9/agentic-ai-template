"""
App entry point.
"""
from fastapi import FastAPI
from routers import rag


app = FastAPI()
app.include_router(rag.router)
# gunicorn -k uvicorn.workers.UvicornWorker main:app

# python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
# In browser, go to: http://127.0.0.1:8000/docs
