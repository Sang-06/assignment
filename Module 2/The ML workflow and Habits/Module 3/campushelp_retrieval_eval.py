"""

campushelp_retrieval_eval.py



A small CampusHelp retrieval evaluator.

Defines a fixed policy corpus, a frozen eval set with expected documents,

runs a simple keyword retriever at top-k = 3, and prints an informal hit rate.



No LLM, no vector database -- pure Python standard library.

"""



# ---------------------------------------------------------------------

# 1. Fixed policy corpus

# ---------------------------------------------------------------------

CORPUS = {

  "D1": (

    "Attendance: Students must maintain at least 75% attendance in "

    "each course to be eligible to sit for the end semester exam. "

    "Attendance below 75% requires a medical certificate for condonation."

  ),

  "D2": (

    "Late Submission: Assignments submitted after the deadline will "

    "incur a 10 percent penalty per day for up to three days. "

    "Submissions more than three days late will not be accepted."

  ),

  "D3": (

    "Library Hours: The central library is open from 8 AM to 10 PM "

    "on weekdays and 9 AM to 6 PM on weekends. Library access "

    "requires a valid student ID card."

  ),

  "D4": (

    "Hostel Mess Refund: Students who wish to opt out of the hostel "

    "mess for more than seven consecutive days must apply for a mess "

    "refund at least three days in advance. Refunds are credited "

    "within two weeks."

  ),

  "D5": (

    "Wi-Fi Access: Campus Wi-Fi is available to all registered "

    "students using their student ID as login credentials. Wi-Fi "

    "speed is capped at 10 Mbps per device in hostel rooms."

  ),

}





# ---------------------------------------------------------------------

# 2. Frozen eval set

# ---------------------------------------------------------------------

EVAL_SET = [

  {

    "qid": "Q1",

    "question": "What is the minimum attendance percentage required to sit for exams?",

    "expected_docs": ["D1"],

  },

  {

    "qid": "Q2",

    "question": "Is there a penalty for submitting an assignment late?",

    "expected_docs": ["D2"],

  },

  {

    "qid": "Q3",

    "question": "What are the library hours on weekdays?",

    "expected_docs": ["D3"],

  },

  {

    "qid": "Q4",

    "question": "How do I get a refund if I leave the hostel mess for a week?",

    "expected_docs": ["D4"],

  },

  {

    "qid": "Q5",

    "question": "How can I connect to the campus Wi-Fi?",

    "expected_docs": ["D5"],

  },

  {

    "qid": "Q6",

    "question": "What is the hostel room rent for a semester?",

    "expected_docs": [], # not covered by the corpus

  },

]





# ---------------------------------------------------------------------

# 3. Simple keyword retriever

# ---------------------------------------------------------------------

def tokenize(text: str) -> list:

  """Lowercase word tokens (letters/digits only, split on everything else)."""

  word = ""

  tokens = []

  for ch in text.lower():

    if ch.isalnum():

      word += ch

    else:

      if word:

        tokens.append(word)

        word = ""

  if word:

    tokens.append(word)

  return tokens





def score_doc(query: str, doc_text: str) -> int:

  """Score = count of query words that also appear in the doc text."""

  query_words = set(tokenize(query))

  doc_words = set(tokenize(doc_text))

  return len(query_words & doc_words)





def retrieve_top_k(query: str, corpus: dict, k: int) -> list:

  """Return the top-k doc IDs from corpus, ranked by score_doc (desc)."""

  scored = [(doc_id, score_doc(query, text)) for doc_id, text in corpus.items()]

  scored.sort(key=lambda pair: pair[1], reverse=True)

  top_ids = [doc_id for doc_id, score in scored[:k]]

  return top_ids





# ---------------------------------------------------------------------

# 4. Scoring helpers

# ---------------------------------------------------------------------

def is_hit(retrieved_doc_ids: list, expected_docs: list):

  """True if any expected doc was retrieved; None if unanswerable (empty expected_docs)."""

  if not expected_docs:

    return None

  return any(doc_id in retrieved_doc_ids for doc_id in expected_docs)





def retrieval_hit_rate(rows: list) -> float:

  """hits / answerable questions only (skips rows where hit is None)."""

  answerable = [row for row in rows if row["hit"] is not None]

  if not answerable:

    return 0.0

  hits = sum(1 for row in answerable if row["hit"] is True)

  return hits / len(answerable)





# ---------------------------------------------------------------------

# 5. Run retrieval + print results

# ---------------------------------------------------------------------

if __name__ == "__main__":

  K = 3

  rows = []



  for item in EVAL_SET:

    qid = item["qid"]

    question = item["question"]

    expected_docs = item["expected_docs"]



    retrieved = retrieve_top_k(question, CORPUS, K)

    hit = is_hit(retrieved, expected_docs)



    rows.append({"qid": qid, "hit": hit})



    hit_label = "N/A" if hit is None else ("HIT" if hit else "MISS")



    print(f"{qid}: {question}")

    print(f" Expected docs : {expected_docs}")

    print(f" Retrieved (k={K}): {retrieved}")

    print(f" Result    : {hit_label}")

    print()



  rate = retrieval_hit_rate(rows)

  print(f"Overall hit rate (Q1-Q5): {rate:.2f} ({rate * 100:.1f}%)")