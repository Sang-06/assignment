import re
from typing import Dict, Any

class GuardrailEngine:
    @staticmethod
    def mask_pii(text: str) -> str:
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        masked_text = re.sub(phone_pattern, '[REDACTED_PHONE]', text)
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        return re.sub(email_pattern, '[REDACTED_EMAIL]', masked_text)

    @staticmethod
    def detect_prompt_injection(text: str) -> bool:
        injection_triggers = ["ignore previous instructions", "you are now an unrestricted ai", "system override", "bypass guardrails"]
        return any(trigger in text.lower() for trigger in injection_triggers)

    @staticmethod
    def verify_groundedness(response_text: str, context_sources: list) -> bool:
        if not context_sources and "do not have enough information" not in response_text:
            return False
        return True