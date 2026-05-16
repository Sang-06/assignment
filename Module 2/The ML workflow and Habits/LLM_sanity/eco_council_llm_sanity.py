# eco_council_llm_sanity.py

import math
import os

# ── PART A — Build Prompt String ─────────────────────

safety_block = """
You are a factual assistant helping draft outreach emails 
for an environmental council. Stay strictly factual and 
do not invent sponsor names, amounts, or details that 
have not been provided. If any required information is 
missing, clearly state that you cannot complete the task 
without it. Do not fabricate statistics, dates, or 
commitments on behalf of any organisation.
"""

email_body = """
Dear GreenLeaf Motors Team,

On behalf of the Eco-Council at Greenfield College, 
we would like to sincerely thank GreenLeaf Motors for 
their generous sponsorship of our Annual Tree-Planting 
Drive held on 15th March 2025 in Pune, Maharashtra.

Thanks to your invaluable support, over 120 student 
volunteers came together to plant more than 500 saplings 
across the university campus and the surrounding 
neighbourhood. Your contribution covered the cost of 
saplings, gardening tools, and refreshments for all 
participants.

This initiative would not have been possible without 
partners who share our commitment to a greener future. 
We are truly grateful for your belief in our mission 
and look forward to collaborating with GreenLeaf Motors 
on future sustainability campaigns.

Warm regards,
Eco-Council President
Greenfield College
"""

follow_up_instruction = (
    "Please suggest a subject line for this email "
    "that is under 60 characters."
)

# Concatenate — safety → email → follow-up
full_prompt = (
    safety_block
    + "\n\n"
    + email_body
    + "\n\n"
    + follow_up_instruction
)

print("PART A — Prompt built successfully!")
print(f"Safety block words    : {len(safety_block.split())}")
print(f"Email body words      : {len(email_body.split())}")
print(f"Follow-up words       : {len(follow_up_instruction.split())}")

# ── PART B — Token Count with tiktoken ───────────────

import tiktoken

try:
    encoder = tiktoken.encoding_for_model("gpt-4")
except Exception:
    encoder = tiktoken.get_encoding("cl100k_base")
    print("Note: Used fallback encoding cl100k_base")

prompt_tokens = len(encoder.encode(full_prompt))
print(f"\nPrompt tokens (tiktoken): {prompt_tokens}")

# ── PART C — Completion Budget Estimate ──────────────

completion_words = 220

# Formula: tokens = words / 0.75 (1 token ≈ 0.75 words)
completion_tokens_est = completion_words / 0.75

print(f"\nEstimated completion tokens (rule of thumb): {completion_tokens_est}")

# ── PART D — Context Window Check ────────────────────

CONTEXT_LIMIT = 4096

# Round up completion tokens for fit test
completion_tokens_rounded = math.ceil(completion_tokens_est)

total_tokens = prompt_tokens + completion_tokens_rounded

fits = total_tokens <= CONTEXT_LIMIT

print(f"\nTotal tokens needed (rounded-up completion): {total_tokens}")
print(f"Fits in 4096 window? {fits}")

# ── PART E — Concept Recall ───────────────────────────

print("\n" + "=" * 60)
print("PART E — Why does AI give different answers each time?")
print("=" * 60)

print("""
When a large language model generates a response, it does 
not retrieve a fixed answer from memory. Instead, at every 
step it calculates a probability distribution over all 
possible next tokens and samples from that distribution. 
This means even with an identical prompt, the model may 
pick a different token at the first step, which changes 
the entire trajectory of the reply. The temperature setting 
controls how sharp or flat this distribution is — lower 
values make high-probability tokens dominate, while higher 
values allow more surprising choices, producing more varied 
and creative outputs across repeated calls.
""")

# ── PART F — Temperature Demo ─────────────────────────

print("=" * 60)
print("PART F — Temperature Demo")
print("=" * 60)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if OPENAI_API_KEY:
    # Uses client.chat.completions.create
    # API key read from environment variable OPENAI_API_KEY
    from openai import OpenAI

    client = OpenAI(api_key=OPENAI_API_KEY)

    user_message = "Describe how is the cloud today??"

    # First call — low temperature = safe and predictable
    response_low = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_message}],
        temperature=0.2
    )

    # Second call — high temperature = creative and varied
    response_high = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_message}],
        temperature=0.9
    )

    print("\n--- temperature=0.2 ---")
    print(response_low.choices[0].message.content)

    print("\n--- temperature=0.9 ---")
    print(response_high.choices[0].message.content)

else:
    print(
        "Skipping live temperature demo — "
        "set OPENAI_API_KEY to enable."
    )

print("\n✅ All Parts Complete!") 