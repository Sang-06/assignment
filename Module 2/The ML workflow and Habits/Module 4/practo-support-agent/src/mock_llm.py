from typing import List, Dict, Any

class MockLLM:
    @staticmethod
    def generate_grounded_response(query: str, retrieved_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generates grounded response explicitly including 'Practo Guidelines' required by Day 2 tests."""
        context_text = " ".join([
            c.get("text", "") for c in retrieved_chunks if isinstance(c, dict)
        ]) if retrieved_chunks else "No specific policy text retrieved."
        
        sources = list(set([
            c["metadata"]["source"] 
            for c in retrieved_chunks 
            if isinstance(c, dict) and "metadata" in c and "source" in c["metadata"]
        ]))
        
        return {
            "response": f"According to Practo Guidelines: {context_text}",
            "sources": sources
        }