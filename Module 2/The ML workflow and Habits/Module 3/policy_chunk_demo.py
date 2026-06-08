"""
ShopEasy Policy Chunk Demo
--------------------------
Splits two short policies into chunks, stores them in Chroma,
and answers a customer question using semantic search.
"""

# ── Imports ──────────────────────────────────────────────────────────────────
import uuid
import chromadb
from sentence_transformers import SentenceTransformer

# ══════════════════════════════════════════════════════════════════════════════
# SAMPLE CORPUS
# ══════════════════════════════════════════════════════════════════════════════

sample_corpus = [
    {
        "source_id": "returns_policy.txt",
        "text": (
            "ShopEasy Returns Policy\n\n"
            "At ShopEasy, customer satisfaction is our top priority. "
            "If you are not completely satisfied with your purchase, you may return most items within 30 days "
            "of the delivery date for a full refund or exchange.\n\n"
            "To be eligible for a return, items must be unused, in the same condition that you received them, "
            "and in the original packaging. Proof of purchase is required for all returns.\n\n"
            "To initiate a return, please contact our customer support team at support@shopeasy.com or "
            "call 1-800-SHOPEASY. Our team will provide you with a Return Merchandise Authorization (RMA) number "
            "and return shipping instructions.\n\n"
            "Refunds will be processed within 5–7 business days after we receive and inspect the returned item. "
            "Refunds are issued to the original payment method. Shipping costs are non-refundable unless the return "
            "is due to our error (e.g., wrong or defective item).\n\n"
            "Certain items are non-returnable, including perishable goods, digital downloads, gift cards, "
            "and items marked as final sale. For hygiene reasons, undergarments and swimwear are also non-returnable "
            "unless defective."
        ),
    },
    {
        "source_id": "shipping_policy.txt",
        "text": (
            "ShopEasy Shipping Policy\n\n"
            "ShopEasy offers a variety of shipping options to meet your needs. "
            "Standard shipping typically takes 5–7 business days, while expedited shipping takes 2–3 business days. "
            "Overnight shipping is available for orders placed before 12:00 PM local time.\n\n"
            "Free standard shipping is available on all orders over $50. Orders below $50 incur a flat shipping fee "
            "of $4.99 for standard delivery.\n\n"
            "Once your order has shipped, you will receive a confirmation email with a tracking number. "
            "You can track your order on our website or through the carrier's tracking portal.\n\n"
            "ShopEasy ships to all 50 US states as well as select international destinations. "
            "International shipping rates and delivery times vary by country. "
            "Customers are responsible for any customs duties or import taxes applicable in their country.\n\n"
            "In the event of a lost or damaged shipment, please contact our support team within 7 days of the "
            "expected delivery date. We will work with the carrier to investigate and resolve the issue promptly."
        ),
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — CHUNKING
# ══════════════════════════════════════════════════════════════════════════════

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 75) -> list[str]:
    """Split *text* into overlapping character-level chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start += chunk_size - overlap  # slide forward with overlap
    return chunks


def create_chunks_from_corpus(
    corpus: list[dict],
    chunk_size: int = 500,
    overlap: int = 75,
) -> list[dict]:
    """
    Iterate over corpus documents, chunk each one, and return a flat list of
    chunk dicts with keys: id, document, metadata.
    """
    all_chunks = []
    for doc in corpus:
        source_id = doc["source_id"]
        raw_chunks = chunk_text(doc["text"], chunk_size=chunk_size, overlap=overlap)
        for idx, chunk in enumerate(raw_chunks):
            all_chunks.append(
                {
                    "id": f"{source_id}_chunk_{idx}",
                    "document": chunk,
                    "metadata": {
                        "source_id": source_id,
                        "chunk_index": idx,
                    },
                }
            )
    return all_chunks


# Run chunking
chunks = create_chunks_from_corpus(sample_corpus, chunk_size=500, overlap=75)

print("=" * 60)
print("STEP 1 — Chunking")
print("=" * 60)
print(f"Total chunks created : {len(chunks)}")
example = chunks[0]
print(f"Example chunk id     : {example['id']}")
print(f"Example metadata     : {example['metadata']}")
print()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — STORE IN CHROMA
# ══════════════════════════════════════════════════════════════════════════════

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Build an in-memory Chroma client (no persistence needed for demo)
client = chromadb.Client()

# Create collection without Chroma's built-in embedding function
collection = client.create_collection(
    name="policy_chunks",
    embedding_function=None,   # we supply our own embeddings
)

# Generate embeddings and add to collection
documents  = [c["document"] for c in chunks]
metadatas  = [c["metadata"] for c in chunks]
ids        = [c["id"] for c in chunks]
embeddings = embedder.encode(documents, show_progress_bar=False).tolist()

collection.add(
    ids=ids,
    documents=documents,
    metadatas=metadatas,
    embeddings=embeddings,
)

print("=" * 60)
print("STEP 2 — Chroma Storage")
print("=" * 60)
print(f"collection.count()   : {collection.count()}")
print()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — SEMANTIC SEARCH
# ══════════════════════════════════════════════════════════════════════════════

query = "How many days do I have to return a product?"
query_embedding = embedder.encode([query], show_progress_bar=False).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=2,
    include=["documents", "metadatas", "distances"],
)

print("=" * 60)
print("STEP 3 — Semantic Search")
print("=" * 60)
print(f"Query : {query}\n")

for rank, (doc_id, document, metadata) in enumerate(
    zip(results["ids"][0], results["documents"][0], results["metadatas"][0]), start=1
):
    print(f"Rank {rank}")
    print(f"  id        : {doc_id}")
    print(f"  source_id : {metadata['source_id']}")
    print(f"  document  : {document[:200].strip()}...")
    print()