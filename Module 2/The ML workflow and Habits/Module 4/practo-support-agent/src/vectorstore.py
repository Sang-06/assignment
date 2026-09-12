import os
import glob
from typing import List, Dict, Any
import chromadb
from sentence_transformers import SentenceTransformer

class VectorStoreManager:
    def __init__(self, collection_name: str = "practo_fixed"):
        self.client = chromadb.Client()
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def ingesting_kb(self, kb_dir: str = "data/kb_documents", strategy: str = "fixed_size"):
        doc_files = glob.glob(os.path.join(kb_dir, "*.txt"))
        documents = []
        metadatas = []
        ids = []
        
        chunk_idx = 0
        for filepath in doc_files:
            filename = os.path.basename(filepath)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
                
            if strategy == "fixed_size":
                # Fixed size chunking (150 chars, 30 overlap)
                step = 120
                for i in range(0, len(text), step):
                    chunk = text[i:i+150]
                    if len(chunk) > 20:
                        documents.append(chunk)
                        metadatas.append({"source": filename})
                        ids.append(f"doc_{chunk_idx}")
                        chunk_idx += 1
            else:
                # Sentence based chunking
                sentences = text.split(". ")
                for s in sentences:
                    if len(s.strip()) > 10:
                        documents.append(s.strip())
                        metadatas.append({"source": filename})
                        ids.append(f"doc_{chunk_idx}")
                        chunk_idx += 1
                        
        embeddings = self.model.encode(documents).tolist()
        self.collection.add(documents=documents, metadatas=metadatas, ids=ids, embeddings=embeddings)

    def query_kb(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        query_emb = self.model.encode([query]).tolist()
        res = self.collection.query(query_embeddings=query_emb, n_results=top_k)
        
        chunks = []
        if res and res["documents"] and res["documents"][0]:
            for i in range(len(res["documents"][0])):
                chunks.append({
                    "text": res["documents"][0][i],
                    "metadata": res["metadatas"][0][i],
                    "distance": res["distances"][0][i] if "distances" in res and res["distances"] else 0.0
                })
        return chunks

def evaluate_retrieval_precision_recall(query: str, ground_truth_doc: str, vsm: VectorStoreManager, top_k: int = 3):
    chunks = vsm.query_kb(query, top_k=top_k)
    retrieved_docs = list(set([c["metadata"]["source"] for c in chunks]))
    
    hits = 1 if ground_truth_doc in retrieved_docs else 0
    precision = hits / len(retrieved_docs) if retrieved_docs else 0.0
    recall = hits / 1.0  # single ground truth target
    return {"precision": precision, "recall": recall, "retrieved_docs": retrieved_docs}