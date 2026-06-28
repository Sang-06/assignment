import json
import re

REQUIRED_KEYS = ["category", "priority", "summary", "needs_human", "suggested_reply"]
ALLOWED_CATEGORIES = {"billing", "shipping", "product", "other"}
ALLOWED_PRIORITIES = {"low", "medium", "high"}

def strip_markdown_fences(text: str) -> str:
    cleaned = text.strip()
    match = re.match(r"^```(?:json)?\s*([\s\S]*?)\s*```$", cleaned, flags=re.IGNORECASE)
    return match.group(1).strip() if match else cleaned

def extract_json_object(text: str) -> str:
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object braces found in model output.")
    return text[start : end + 1]

def safe_parse_model_json(raw: str) -> dict:
    step1 = strip_markdown_fences(raw)
    step2 = extract_json_object(step1)
    data = json.loads(step2)
    if not isinstance(data, dict):
        raise ValueError("Top-level JSON must be an object (dict).")
    return data

def validate_ticket(data: dict) -> tuple[bool, str]:
    """
    Validates the parsed ticket data dictionary against the business logic rules.
    Checks must run strictly in the specified order.
    """
    # 1. Check if all required keys are present
    for key in REQUIRED_KEYS:
        if key not in data:
            return False, f"Missing required key: '{key}'"
            
    # 2. Check if the category is allowed
    if data["category"] not in ALLOWED_CATEGORIES:
        return False, f"Invalid category: '{data['category']}'"
        
    # 3. Check if the priority is allowed
    if data["priority"] not in ALLOWED_PRIORITIES:
        return False, f"Invalid priority: '{data['priority']}'"
        
    return True, "ok"

def validate_or_raise(data: dict) -> dict:
    """
    Wraps validate_ticket. Raises a ValueError on failure, 
    otherwise returns the clean dictionary data.
    """
    is_valid, reason = validate_ticket(data)
    if not is_valid:
        raise ValueError(reason)
    return data

TEST_CASES = [
    # Case 1 — valid ticket (should print SUCCESS)
    '{"category": "shipping", "priority": "medium", "summary": "Order 4412 arrived late", '
    '"needs_human": false, "suggested_reply": "We are tracking your parcel."}',
    # Case 2 — wrong priority casing (should print FAILED)
    '{"category": "billing", "priority": "HIGH", "summary": "Duplicate charge", '
    '"needs_human": false, "suggested_reply": "Refund initiated."}',
]

def main() -> None:
    """
    Loops over the test cases, running the safe parser followed by the validator layer.
    """
    for raw_string in TEST_CASES:
        try:
            # Parse out raw string text safely into a dict
            parsed_dict = safe_parse_model_json(raw_string)
            # Run validation layer
            validated_dict = validate_or_raise(parsed_dict)
            print(f"SUCCESS: {validated_dict}")
        except ValueError as e:
            print(f"FAILED: {e}")

if __name__ == "__main__":
    main()