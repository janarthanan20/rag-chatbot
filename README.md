# RAG Chatbot over PDF Documents

A small Retrieval-Augmented Generation (RAG) chatbot in Python. It answers questions
**only** from your PDFs and says "I don't know" when the answer isn't there.

## How it works
1. `ingest.py` reads PDFs in `docs/`, splits them into overlapping chunks, and stores them in a Chroma vector database.
2. `chat.py` takes a question, retrieves the 4 most relevant chunks, and sends them with the question to an LLM.
3. The prompt forces the model to answer from the context and cite file + page.
4. `test_rag.py` runs 10 test cases (factual, multi-point, out-of-scope, prompt-injection) and saves `test_results.csv`.

## Stack
Python, ChromaDB (vector store + embeddings), pypdf, OpenAI-compatible LLM API, prompt engineering.

## Run it
```bash
pip install -r requirements.txt
cp .env.example .env        # add your API key
# put 2-3 PDFs in docs/
python ingest.py
python chat.py
python test_rag.py
```

## Test results
Pass rate: _fill in after running_  (see `test_results.csv`)

## Improvements I made after testing
- _fill in, e.g. changed chunk size, tightened the system prompt, increased TOP_K_
