"""
FinSight Analytics — Mini Grounded RAG
=======================================
Retrieve → Augment → Generate pipeline using:
  - LangChain + Chroma for vector retrieval
  - HuggingFace sentence-transformers for embeddings
  - Groq (llama-3.3-70b-versatile) for grounded generation
"""

import os
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from groq import Groq

# ── CORPUS ────────────────────────────────────────────────────────────────────

CORPUS = [
    {
        "text": (
            "NovaTech Annual Report 2022 — Financial Highlights. "
            "Total revenue for fiscal year 2022 was 48.2 billion dollars, "
            "representing 19 percent year-over-year growth."
        ),
        "metadata": {"source_id": "novatech_2022.pdf", "page": 12},
    },
    {
        "text": (
            "NovaTech Annual Report 2022 — Operating Income. "
            "Operating income reached 6.1 billion dollars in 2022. "
            "Cloud services contributed the largest share of margin improvement."
        ),
        "metadata": {"source_id": "novatech_2022.pdf", "page": 18},
    },
    {
        "text": (
            "NovaTech Annual Report 2023 — Outlook. "
            "Management expects continued investment in AI infrastructure through 2024. "
            "No weather or macro-forecast data is included in this document."
        ),
        "metadata": {"source_id": "novatech_2023.pdf", "page": 4},
    },
    {
        "text": (
            "NovaTech Annual Report 2022 — Employee Count. "
            "NovaTech employed 124000 people worldwide at the end of 2022."
        ),
        "metadata": {"source_id": "novatech_2022.pdf", "page": 31},
    },
]

# ── SYSTEM MESSAGE ────────────────────────────────────────────────────────────

SYSTEM_MESSAGE = """You are FinSight, a grounded financial analyst assistant.

Rules:
1. Answer ONLY using information found in the #context section below.
2. If the answer is not present in the context, respond with:
   "I don't know — this information is not available in the provided documents."
3. Do NOT use any external knowledge, assumptions, or hallucinations.
4. Be concise and cite the source document when possible.

The user message is structured with two delimiters:
  #context  — the retrieved document chunks relevant to the question
  #question — the user's actual question to answer
"""

# ── STEP 1 — BUILD VECTOR INDEX ───────────────────────────────────────────────

def build_index(corpus, persist_directory="./mini_report_db"):
    """Convert corpus records to LangChain Documents and persist in Chroma."""
    documents = [
        Document(page_content=record["text"], metadata=record["metadata"])
        for record in corpus
    ]

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory,
    )

    print("=" * 60)
    print("STEP 1 — Vector Index Built")
    print("=" * 60)
    print(f"Total documents stored : {vectorstore._collection.count()}")
    print()

    return vectorstore


# ── STEP 2 — CONFIGURE RETRIEVER ─────────────────────────────────────────────

def build_retriever(vectorstore, k=3):
    """Create a similarity retriever returning top-k chunks."""
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )
    return retriever


# ── STEP 3 — PROMPT ASSEMBLY ──────────────────────────────────────────────────

def build_user_message(user_query: str, retrieved_chunks: list[Document]) -> str:
    """
    Assemble the #context / #question delimited user message.
    """
    context_parts = []
    for i, chunk in enumerate(retrieved_chunks, start=1):
        source = chunk.metadata.get("source_id", "unknown")
        page   = chunk.metadata.get("page", "?")
        context_parts.append(
            f"[Chunk {i} | {source} | page {page}]\n{chunk.page_content}"
        )

    context_block = "\n\n".join(context_parts)

    user_message = (
        f"#context\n{context_block}\n\n"
        f"#question\n{user_query}"
    )
    return user_message


# ── STEP 4 — GROUNDED GENERATION ─────────────────────────────────────────────

def generate_answer(system_message: str, user_message: str) -> str:
    """Call Groq with temperature=0 for deterministic grounded answers."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY not found. Please set it as an environment variable."
        )

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user",   "content": user_message},
        ],
    )
    return response.choices[0].message.content.strip()


def rag_answer(user_query: str, retriever) -> dict:
    """
    Full RAG pipeline:
      1. Retrieve relevant chunks
      2. Build augmented user message
      3. Generate grounded answer

    Returns dict with keys: answer, retrieved_chunks, user_message
    """
    retrieved_chunks = retriever.invoke(user_query)
    user_message     = build_user_message(user_query, retrieved_chunks)
    answer           = generate_answer(SYSTEM_MESSAGE, user_message)

    return {
        "answer":            answer,
        "retrieved_chunks":  retrieved_chunks,
        "user_message":      user_message,
    }


# ── STEP 5 — MAIN ─────────────────────────────────────────────────────────────

def main():
    # Build index and retriever
    vectorstore = build_index(CORPUS)
    retriever   = build_retriever(vectorstore, k=3)

    queries = [
        "What was NovaTech's total revenue in 2022?",
        "What is the weather in Mumbai tomorrow?",
    ]

    for query_label, user_query in zip(["Query A", "Query B"], queries):
        print("=" * 60)
        print(f"STEP 5 — {query_label}")
        print("=" * 60)
        print(f"Question : {user_query}\n")

        result = rag_answer(user_query, retriever)

        # Retrieval trace
        print("── Retrieval Trace ──────────────────────────────────────")
        for i, chunk in enumerate(result["retrieved_chunks"], start=1):
            preview = chunk.page_content[:120].replace("\n", " ")
            print(f"  Chunk {i}")
            print(f"    metadata : {chunk.metadata}")
            print(f"    preview  : {preview}...")
        print()

        # Generated answer
        print("── Generated Answer ─────────────────────────────────────")
        print(f"  {result['answer']}")
        print()


if __name__ == "__main__":
    main()