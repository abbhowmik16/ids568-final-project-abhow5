import time
import requests

queries = [
    "What is RAG?",
    "Why is chunking important?",
    "How do embeddings help retrieval?",
    "What is a vector database?",
    "What does grounding mean?",
    "How should RAG evaluation be done?",
    "What happens when retrieval returns irrelevant chunks?",
    "Why is chunk overlap useful?",
]

url = "http://127.0.0.1:8000/ask"

for i in range(50):
    q = queries[i % len(queries)]
    response = requests.get(url, params={"q": q, "generate": "false"})
    print(i + 1, response.status_code, q)
    time.sleep(0.2)

print("Traffic generation complete.")