from rag import ask

print("RAG chatbot ready. Type 'exit' to quit.")
while True:
    try:
        q = input("\nYou: ").strip()
    except (KeyboardInterrupt, EOFError):
        break
    if not q:
        continue
    if q.lower() in {"exit", "quit"}:
        break
    answer = ask(q).replace("\u2011", "-")
    print("Bot:", answer)