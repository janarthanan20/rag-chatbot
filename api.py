from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag import ask

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
        return Answer(answer=ask(q))
    except Exception:
        raise HTTPException(status_code=502, detail="LLM request failed")