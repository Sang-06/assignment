from src.dataset import generate_appointment_dataset, generate_kb_documents
from src.vectorstore import VectorStoreManager
from src.mock_llm import MockLLM

def test_day1_pipeline():
    records = generate_appointment_dataset()
    assert len(records) >= 40
    
    generate_kb_documents()
    
    vsm = VectorStoreManager()
    vsm.ingesting_kb(strategy="fixed_size")
    retrieved = vsm.query_kb("cancellation full refund", top_k=3)
    assert len(retrieved) > 0
    
    response_data = MockLLM.generate_grounded_response("cancellation full refund", retrieved)
    assert response_data["grounded"] is True
    
    unrelated_retrieved = vsm.query_kb("quantum mechanics physics", top_k=3)
    fallback_data = MockLLM.generate_grounded_response("quantum mechanics physics", unrelated_retrieved)
    assert fallback_data["grounded"] is False
    assert MockLLM.FALLBACK_RESPONSE in fallback_data["response"]
    
    print("\n🎉 Day 1 Verification PASSED successfully!")

if __name__ == "__main__":
    test_day1_pipeline()