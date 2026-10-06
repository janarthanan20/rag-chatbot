"""Core RAG logic: ingest PDFs -> chunk -> embed + store in Chroma -> retrieve -> ask LLM."""
import os, glob
import chromadb
from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
CHUNK_SIZE, OVERLAP, TOP_K = 800, 150, 4

db = chromadb.PersistentClient(path="chroma_db")
collection = db.get_or_create_collection("knowledge")  # Chroma embeds text automatically
llm = OpenAI(api_key=os.getenv("LLM_API_KEY"), base_url=os.getenv("LLM_BASE_URL") or None)
MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")


def chunk(text):
    step = CHUNK_SIZE - OVERLAP
    return [text[i:i + CHUNK_SIZE] for i in range(0, len(text), step) if text[i:i + CHUNK_SIZE].strip()]


def ingest(folder="docs"):
    """Read every PDF in the folder, split into chunks, store with source + page metadata."""
    ids, docs, metas = [], [], []
    for path in glob.glob(f"{folder}/*.pdf"):
        for page_no, page in enumerate(PdfReader(path).pages, start=1):
            for n, piece in enumerate(chunk(page.extract_text() or "")):
                ids.append(f"{os.path.basename(path)}-p{page_no}-c{n}")
                docs.append(piece)
                metas.append({"source": os.path.basename(path), "page": page_no})
    if ids:
        collection.upsert(ids=ids, documents=docs, metadatas=metas)
    print(f"Ingested {len(ids)} chunks from {folder}/")


def ask(question):
    """Retrieve the most relevant chunks and answer ONLY from them."""
    hits = collection.query(query_texts=[question], n_results=TOP_K)
    context = "\n\n".join(
        f"[{m['source']} p.{m['page']}] {d}" for d, m in zip(hits["documents"][0], hits["metadatas"][0])
    )
    system = ("You answer questions using ONLY the context provided. "
              "If the answer is not in the context, reply exactly: I don't know based on the documents. "
              "Keep answers short and mention the source file and page.")
    reply = llm.chat.completions.create(
        model=MODEL, temperature=0,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}],
    )
    return reply.choices[0].message.content
