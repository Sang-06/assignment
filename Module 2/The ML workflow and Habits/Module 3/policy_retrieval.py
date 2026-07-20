"""
policy_retrieval.py

A metadata-first retrieval layer for ShopSphere's product-support
knowledge base. Simulates filter-first retrieval WITHOUT any LLM
or vector database — pure Python standard library.
"""

# ---------------------------------------------------------------------
# Knowledge base
# ---------------------------------------------------------------------
chunks = [
    {
        "text": "Mobiles can be returned within 7 days if damaged.",
        "metadata": {
            "doc_type": "policy",
            "product": "mobile",
            "status": "active",
            "source_file": "mobile_policy.md",
            "section_title": "Return Rules",
        },
    },
    {
        "text": "Laptops can be returned within 10 days for manufacturing defects.",
        "metadata": {
            "doc_type": "policy",
            "product": "laptop",
            "status": "active",
            "source_file": "laptop_policy.md",
            "section_title": "Return Rules",
        },
    },
    {
        "text": "Laptops were earlier returnable within 30 days.",
        "metadata": {
            "doc_type": "policy",
            "product": "laptop",
            "status": "archived",
            "source_file": "old_laptop_policy.md",
            "section_title": "Old Return Rules",
        },
    },
    {
        "text": "For laptop battery drain, run diagnostics mode before replacing parts.",
        "metadata": {
            "doc_type": "manual",
            "product": "laptop",
            "status": "active",
            "source_file": "laptop_service_manual.pdf",
            "section_title": "Battery Diagnostics",
        },
    },
    {
        "text": "Premium users get billing support within 24 hours.",
        "metadata": {
            "doc_type": "policy",
            "product": "billing",
            "status": "active",
            "source_file": "billing_policy.md",
            "section_title": "Premium Support",
        },
    },
]


# ---------------------------------------------------------------------
# 1. Filter matcher
# ---------------------------------------------------------------------
def matches_filters(metadata: dict, filters: dict) -> bool:
    """Return True only when every key in filters matches metadata."""
    for key, value in filters.items():
        if metadata.get(key) != value:
            return False
    return True


# ---------------------------------------------------------------------
# 2. Retrieval
# ---------------------------------------------------------------------
def retrieve(filters: dict) -> list:
    """Return the list of chunks whose metadata passes matches_filters."""
    results = []
    for chunk in chunks:
        if matches_filters(chunk["metadata"], filters):
            results.append(chunk)
    return results


# ---------------------------------------------------------------------
# 3. Citation formatter
# ---------------------------------------------------------------------
def format_citation(chunk: dict) -> str:
    """Return 'Source: <source_file> - <section_title>'."""
    source_file = chunk["metadata"]["source_file"]
    section_title = chunk["metadata"]["section_title"]
    return f"Source: {source_file} - {section_title}"


# ---------------------------------------------------------------------
# 4. Print results
# ---------------------------------------------------------------------
def print_retrieval_results(filters: dict) -> None:
    """Print text + citation for every matching chunk, or a not-found message."""
    results = retrieve(filters)
    if not results:
        print("No matching chunks found.")
        return
    for chunk in results:
        print(chunk["text"])
        print(format_citation(chunk))
        print()


# ---------------------------------------------------------------------
# 5. Demo block
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print_retrieval_results({"doc_type": "policy", "product": "laptop", "status": "active"})
    print_retrieval_results({"doc_type": "policy", "product": "mobile", "status": "active"})
    print_retrieval_results({"doc_type": "manual", "product": "laptop", "status": "active"})