from typing import List, Dict

class ChunkingEngine:
    
    @staticmethod
    def fixed_size_chunking(text: str, chunk_size: int = 200, overlap: int = 30) -> List[Dict[str, str]]:
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = min(start + chunk_size, text_length)
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append({"text": chunk_text, "strategy": "fixed_size"})
            if end == text_length:
                break
            start += (chunk_size - overlap)
            
        return chunks

    @staticmethod
    def sentence_chunking(text: str) -> List[Dict[str, str]]:
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        chunks = []
        for line in lines:
            chunks.append({"text": line, "strategy": "sentence"})
        return chunks