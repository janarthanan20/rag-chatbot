from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag import ask
from db import log_query, recent_queries

app = FastAPI(title="RAG Chatbot API")


class Question(BaseModel):
    question: str


class Answer(BaseModel):
    answer: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=Answer)
def ask_question(body: Question):
    q = body.question.strip()
    if not q:
        raise HTTPException(status_code=400, detail="Question must not be empty")
    try:
        answer = ask(q)
    except Exception:
        raise HTTPException(status_code=502, detail="LLM request failed")
    log_query(q, answer)
    return Answer(answer=answer)


@app.get("/history")
def history(limit: int = 10):
    return recent_queries(limit)