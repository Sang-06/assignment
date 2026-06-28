import sys
import tiktoken  # <--- Added the official library import here

# Simulated historical chat log for the GreenCart support agent
CHAT_HISTORY = [
    {"role": "system", "content": "Use only GreenCart policy FAQ facts."},
    {"role": "user", "content": "Hi, what is your return window?"},
    {"role": "assistant", "content": "Our return window is 30 days from purchase."},
    {"role": "user", "content": "Great, does that cover electronics too?"},
    {"role": "assistant", "content": "Electronics have a shorter 14-day window."},
    {"role": "user", "content": "Okay, what about shipping fees for returns?"},
    {"role": "assistant", "content": "Returns are free if you use our pre-paid label."},
    {"role": "user", "content": "Awesome, thanks for the help!"}
]

def calculate_token_metrics(text: str) -> tuple[int, int]:
    """
    TODO 1: Calculate word count and approximate token count.
    Standard rule of thumb: 1 word is roughly 1.33 tokens.
    """
    words = text.split()
    word_count = len(words)
    
    # Standard engineering approximation for LLM tokens (1 word ~ 1.33 tokens)
    token_count = int(word_count * 1.33)
    
    return word_count, token_count

def apply_window_budget(history: list[dict], max_messages: int) -> tuple[list[dict], list[dict]]:
    """
    TODO 2: Slice the history to keep only the newest max_messages.
    Return a tuple of (kept_messages, dropped_messages).
    """
    if len(history) <= max_messages:
        return history, []
        
    # The split point: everything up to index is dropped, everything after is kept
    split_index = len(history) - max_messages
    dropped_messages = history[:split_index]
    kept_messages = history[split_index:]
    
    return kept_messages, dropped_messages

if __name__ == "__main__":
    # 1. Evaluate the token usage of the system's core grounding rule
    system_instruction = CHAT_HISTORY[0]["content"]
    w_count, t_count = calculate_token_metrics(system_instruction)
    
    print("=== Token check ===")
    print(f"Word count: {w_count}")
    print(f"Token count: {t_count}")
    
    # 2. Apply a strict sliding context window of maximum 4 messages
    max_window = 4
    kept, dropped = apply_window_budget(CHAT_HISTORY, max_window)
    
    print(f"=== Windowed history (max {max_window} messages) ===")
    print(f"Messages sent to model: {len(kept)}")
    print(f"Messages dropped: {len(dropped)}")
    
    if dropped:
        # Extract the content text of the earliest message that had to be cut
        first_dropped_text = dropped[0]["content"]
        print(f"First dropped message: {first_dropped_text}")