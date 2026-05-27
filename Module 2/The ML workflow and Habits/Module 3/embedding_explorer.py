from sentence_transformers import SentenceTransformer
 
# Load the model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
 
# Four required sentences
sentences = [
    "How do I return a product?",
    "What is the refund policy?",
    "When is the Module 3 capstone viva?",
    "Refunds are processed within seven working days.",
]
 
# Convert sentences to embeddings
embeddings = model.encode(sentences)
 
# Print summary
print("--- Mini Text Embedding Explorer ---")
for sentence, embedding in zip(sentences, embeddings):
    print(f"\nSentence: {sentence}")
    print(f"Vector length: {len(embedding)}")
    print(f"First 5 numbers: {[round(float(x), 6) for x in embedding[:5]]}")
 
# RAG explanation
print("\n--- RAG Connection ---")
print("Each sentence can become a document chunk in a RAG library.")
print("The embeddings can later be stored in a vector database.")
print("When a user asks a question, similar chunks can be retrieved and added to the prompt.")