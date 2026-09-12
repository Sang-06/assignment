# Practo Support Agent — Multi-Day Agentic AI Workflow

A resilient, multi-day support agent pipeline built with **LangGraph**, **RAG**, **PII Guardrails**, and **Model Context Protocol (MCP)** tool integration, designed to operate under \MockLLM\ with **zero external API key requirements**.

---

## ??? System Architecture

\\\	ext
                                    +-----------------------+
                                    |    User Support Query |
                                    +-----------+-----------+
                                                |
                                                v
                                    +-----------------------+
                                    |   Guardrail Engine    |
                                    |  - PII Redaction      |
                                    |  - Prompt Injection   |
                                    +-----------+-----------+
                                                |
                                                v
                                    +-----------------------+
                                    |   LangGraph Agent     |
                                    +-----------+-----------+
                                                |
                       +------------------------+------------------------+
                       |                                                 |
                       v                                                 v
        +-----------------------------+                   +-----------------------------+
        |  Appointment Lookup Node    |                   |    RAG Retrieval Node       |
        |  - AgentTools Integration   |                   |    - Knowledge Base Chunks  |
        |  - Escalation Calculation   |                   |    - Fixed Vector Store     |
        +--------------+--------------+                   +--------------+--------------+
                       |                                                 |
                       +------------------------+------------------------+
                                                |
                                                v
                                    +-----------------------+
                                    |   Generation Node     |
                                    |   - Grounded Response |
                                    |   - MockLLM Engine    |
                                    +-----------------------+
\\\

---

## ??? Key Features & Components

* **Dataset Generator (\dataset.py\)**: Generates structured mock appointment records (\data/appointments.json\) and policy knowledge-base documents (\data/kb_documents.json\).
* **PII Guardrails & Security (\src/guardrails.py\)**: Redacts sensitive personal information (phone numbers, email addresses, IDs) and detects prompt injection attempts before query processing.
* **LangGraph Pipeline (\src/agent.py\)**: Coordinates query flow between PII masking, appointment status lookup, vector database query retrieval, and answer generation.
* **Escalation Logic (\src/tools.py\)**: Computes escalation scores dynamically using the formula:
  main\text{Escalation Score} = 0.6 \times \text{follow\_up\_required} + 0.4 \times \left(\frac{\text{days\_since\_created}}{30}\right)main
* **MCP Integration (\src/mcp_server.py\, \src/mcp_client.py\)**: Exposes appointment lookups and escalation score calculations via standard Model Context Protocol server tools.
* **Zero API Dependency (\src/mock_llm.py\)**: Operates entirely using deterministic grounded mock generation without requiring external API keys.

---

## ?? Running Verification Tests

Run the full day-by-day test suite using Python's module runner:

\\\ash
# Day 1: Dataset Generation & Vector Store Verification
python -m tests.test_day1

# Day 2: LangGraph Agent, Guardrails & RAG Pipeline Verification
python -m tests.test_day2

# Day 3: MCP Tool Integration & Production Endpoint Verification
python -m tests.test_day3
\\\

---

## ?? Repository Structure

\\\	ext
practo-support-agent/
+-- data/
¦   +-- dataset.py            # Synthetic data generation logic
¦   +-- appointments.json     # Generated appointment records
¦   +-- kb_documents.json     # Policy documents knowledge base
+-- src/
¦   +-- agent.py              # PractoLangGraphAgent state machine
¦   +-- guardrails.py         # GuardrailEngine (PII & injection detection)
¦   +-- mcp_client.py         # Client interface for MCP tools
¦   +-- mcp_server.py         # MCPServer exposing agent tools
¦   +-- mock_llm.py           # Mock LLM for grounded text output
¦   +-- tools.py              # AgentTools static utility methods
¦   +-- vectorstore.py        # VectorStoreManager for KB indexing
+-- tests/
¦   +-- test_day1.py          # Day 1 test suite
¦   +-- test_day2.py          # Day 2 test suite
¦   +-- test_day3.py          # Day 3 test suite
+-- README.md
\\\
"@


