import os
import logging
import sys
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log

# ==========================================
# 1. LOGGING CONFIGURATION
# ==========================================
# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Define standard format matching requirements
log_format = "%(asctime)s | %(levelname)s | %(message)s"

# Setup the root logger
logger = logging.getLogger("shopeasy_retry")
logger.setLevel(logging.INFO)

# Clear any pre-existing handlers to prevent double logging logs
if logger.hasHandlers():
    logger.handlers.clear()

# File Handler (writes to logs/api_retries.log)
file_handler = logging.FileHandler(os.path.join("logs", "api_retries.log"))
file_handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(file_handler)

# Console Handler (prints out directly to stdout)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(console_handler)

# ==========================================
# 2. STATE TRACKING & CORE LOGIC
# ==========================================
# State counter to track live function execution attempts
api_state = {
    "attempts": 0
}

@retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    before_sleep=before_sleep_log(logger, logging.WARNING)
)
def lookup_order_status(order_id: str) -> str:
    """
    Simulates a flaky e-commerce order API that experiences throttling
    under peak Diwali traffic before resolving successfully.
    """
    # Increment execution tracker state
    api_state["attempts"] += 1
    
    # Fail on the first two calls with HTTP 429 Throttle exception
    if api_state["attempts"] <= 2:
        raise Exception("HTTP 429 Too Many Requests")
        
    # Return specific exact output string on the third call
    return f"Order {order_id} — out for delivery. Expected by 6 PM today."

# ==========================================
# 3. RUNTIME EXECUTION BLOCK
# ==========================================
if __name__ == "__main__":
    try:
        # Execute the wrapper system function
        status_result = lookup_order_status("ORD-7842")
        
        # Print output string matches expected formatting
        print(status_result)
        print(f"Total API attempts: {api_state['attempts']}")
        
    except Exception as final_exception:
        logger.error(f"Application crashed unexpectedly: {final_exception}")