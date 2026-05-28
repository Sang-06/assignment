import chromadb
from sentence_transformers import SentenceTransformer
from pprint import pprint
 
# ── SETUP ──────────────────────────────────────────────────────────────────────
 
# Create persistent Chroma client — data is saved to disk in ./chroma_store
client = chromadb.PersistentClient(path="./chroma_store")
 
# Open or create collection — embedding_function=None because we handle embeddings
# ourselves using SentenceTransformer (gives us full control over the model used)
collection = client.get_or_create_collection(
    name="support_knowledge_base",
    embedding_function=None
)
 
# ── KNOWLEDGE BASE DATA ────────────────────────────────────────────────────────
 
ids = ["doc1", "doc2", "doc3", "doc4", "doc5"]
 
documents = [
    "Customers can return products within 30 days of delivery.",
    "Refunds are processed within 5 to 7 business days after the return is approved.",
    "Orders above 499 rupees qualify for free shipping.",
    "You can reset your password from the account settings page.",
    "Express delivery orders usually arrive within 24 to 48 hours.",
]
 
metadatas = [
    {"category": "returns"},
    {"category": "returns"},
    {"category": "shipping"},
    {"category": "account"},
    {"category": "shipping"},
]
 
# ── LOAD MODEL & BUILD EMBEDDINGS ─────────────────────────────────────────────
 
# The SAME embedding model must encode both stored FAQs and every user query
# because embeddings only have consistent meaning within the same model's vector space.
# Using different models would produce incompatible vectors and break similarity search.
model = SentenceTransformer("all-MiniLM-L6-v2")
 
# Encode all documents and convert numpy arrays to plain Python lists for Chroma
document_embeddings = model.encode(documents).tolist()
 
# ── UPSERT & VERIFY ───────────────────────────────────────────────────────────
 
# upsert = insert if new, update if id already exists (safe to re-run)
collection.upsert(
    ids=ids,
    documents=documents,
    metadatas=metadatas,
    embeddings=document_embeddings
)
 
print("=" * 60)
print(f"Collection name : {collection.name}")
print(f"Document count  : {collection.count()}")   # expect 5
print("=" * 60)
 
# peek() returns a quick sample of stored records (default first 10)
# get()  retrieves specific records by id — no vector search involved
print("\n--- peek() sample ---")
pprint(collection.peek())
 
print("\n--- get(ids=['doc4']) ---")
pprint(collection.get(ids=["doc4"]))
 
# ── SEMANTIC SEARCHES ─────────────────────────────────────────────────────────
 
def semantic_search(query: str, n_results: int, query_num: int):
    """Encode query with the same model, then search by vector similarity."""
    print(f"\n{'=' * 60}")
    print(f"Query {query_num}: {query}")
    print(f"{'=' * 60}")
 
    # Encode user query — MUST use same model as stored embeddings
    query_embedding = model.encode([query]).tolist()
 
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
 
    # Print ranked results
    for rank, (doc_id, document, metadata, distance) in enumerate(zip(
        results["ids"][0],
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ), start=1):
        print(f"\n  Rank     : {rank}")
        print(f"  ID       : {doc_id}")
        print(f"  Document : {document}")
        print(f"  Metadata : {metadata}")
        print(f"  Distance : {round(distance, 6)}")
 
    return results
 
# Query 1 — return + refund intent
semantic_search("I want to return my shoes and get my money back", n_results=3, query_num=1)
 
# Query 2 — password reset intent
semantic_search("How do I change my login password?", n_results=2, query_num=2)
 
# Query 3 — payment method intent (no FAQ exists for this)
results3 = semantic_search("Can I pay with UPI?", n_results=3, query_num=3)
 
# ── GAP ANALYSIS ──────────────────────────────────────────────────────────────
 
top_id       = results3["ids"][0][0]
top_metadata = results3["metadatas"][0][0]
 
print("\n--- Gap analysis ---")
print(f"The top result for the UPI payment query was {top_id}, "
      f"which belongs to the '{top_metadata['category']}' category.")
print(f"Even though {top_id} is the closest vector in this small store, "
      f"it is a weak business answer because no payment-related FAQ exists in the knowledge base — "
      f"the model retrieved the least-dissimilar document rather than a genuinely relevant one, "
      f"meaning a real customer would receive an unhelpful or misleading response.")