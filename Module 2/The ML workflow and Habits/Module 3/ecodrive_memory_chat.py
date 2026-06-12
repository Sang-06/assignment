import json
import os
HISTORY_FILE = "ecodrive_chat_history.json"

#=============================================================
# Part A Save and Load JSON
#=============================================================
def save_history(history):
    """Saves the chat list to a JSON file."""
    with open (HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def load_history():
    """Loads chat history from JSON file. Returns empty list if missing."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []
    

def append_turn(history, user_text, bot_text):
    """Appends user and assistant roles, saves to file, and returns history."""
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": bot_text})
    save_history(history)
    return history

# ==============================================================
# Provided stub (copied exactly)
# ==============================================================

def mock_rag_answer(full_question):
    text = full_question.lower()
    if "2022" in text and "revenue" in text:
        return "EcoDrive revenue in 2022 was 12.4 billion dollars."
    if "2023" in text and ("revenue" in text or "2022" in text):
        return "EcoDrive revenue in 2023 was 14.1 billion dollars."
    return "I need more context about which metric and year you mean."

# =====================================================================
# Part B — One chat turn with memory
# =====================================================================

def chat_once(user_message, history):
    """Builds a conversational string context, queries the RAG, and saves the turn."""
    # Build full_question by joining each role: content line from history
    lines = []
    for turn in history:
        lines.append(f"{turn['role']}: {turn['content']}")
    
    # Append the current user turn to the end of the question context
    lines.append(f"user: {user_message}")
    full_question = "\n".join(lines)
    
    # Call the provided mock_rag_answer inside try/except
    try:
        bot_reply = mock_rag_answer(full_question)
    except Exception:
        bot_reply = "Search is unavailable right now. Please try again in a minute."
    
    # Commit the turn to memory history file
    append_turn(history, user_message, bot_reply)
    
    return bot_reply


# =====================================================================
# Part C — Two-turn demo in main()
# =====================================================================

def main():
    # Delete the JSON file if it exists to start fresh
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
        
    # --- Turn 1 ---
    # Load history (will be an empty list initially)
    history = load_history()
    turn_1_query = "What was EcoDrive revenue in 2022?"
    reply_1 = chat_once(turn_1_query, history)
    print(f"Turn 1: {reply_1}")
    
    # --- Turn 2 ---
    # Reload history from file to prove persistence layer works
    history = load_history()
    turn_2_query = "And in 2023?"
    reply_2 = chat_once(turn_2_query, history)
    print(f"Turn 2: {reply_2}")


if __name__ == "__main__":
    main()