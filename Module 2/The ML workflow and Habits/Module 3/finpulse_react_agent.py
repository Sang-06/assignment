# ============================================================
# FinPulse Research Desk — ReAct Agent
# Single file: finpulse_react_agent.py
# ============================================================

# ============================================================
# STEP 1 — Setup and Tools
# ============================================================
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_classic.agents import Tool, AgentExecutor, create_react_agent
from langchain_experimental.tools import PythonREPLTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.prompts import PromptTemplate

load_dotenv()

# ⚠️ TEMPORARY — Replace with your NEW keys
# DELETE these two lines before submitting to GitHub!
os.environ["GROQ_API_KEY"] = ""
os.environ["SERPER_API_KEY"] = ""


# ============================================================
# STEP 2 — Smoke-test both tools
# ============================================================
def test_tools(repl_tool, search_tool):
    # Test 1: Python REPL — simple math calculation
    print("🐍 Testing Python REPL tool...")
    repl_result = repl_tool.invoke('print(1250 * 1.08)')
    print(f"   REPL Result: {repl_result}")

    # Test 2: Serper Search — simple factual search
    print("\n🔍 Testing Serper Search tool...")
    search_result = search_tool.invoke("Who is the founder of Tesla?")
    print(f"   Search Result (first 120 chars): {str(search_result)[:120]}")


# ============================================================
# STEP 3 — Python-only ReAct Agent (math/calculation)
# ============================================================
def run_python_agent(groq_llm, repl_tool, react_prompt):
    print("\n🤖 Building Python-only ReAct agent...")

    python_agent = create_react_agent(
        llm=groq_llm,
        tools=[repl_tool],
        prompt=react_prompt
    )

    python_executor = AgentExecutor(
        agent=python_agent,
        tools=[repl_tool],
        verbose=True
    )

    query = "If $450 amounts to $630 in 6 years, what will it amount to in 2 years at the same interest rate?"
    print(f"\n📌 Query: {query}\n")
    result = python_executor.invoke({"input": query})
    print(f"\n✅ Final Answer: {result['output']}")


# ============================================================
# STEP 4 — Search + Python ReAct Agent (live market data)
# ============================================================
def run_search_agent(groq_llm, search_tool, repl_tool, react_prompt):
    print("\n🤖 Building Search + Python ReAct agent...")

    search_agent = create_react_agent(
        llm=groq_llm,
        tools=[search_tool, repl_tool],
        prompt=react_prompt
    )

    search_executor = AgentExecutor(
        agent=search_agent,
        tools=[search_tool, repl_tool],
        verbose=True,
        max_iterations=8
    )

    query = "What is the closing stock price of Nifty today?"
    print(f"\n📌 Query: {query}\n")
    result = search_executor.invoke({"input": query})
    print(f"\n✅ Final Answer: {result['output']}")


# ============================================================
# STEP 5 — main() entry point
# ============================================================
def main():

    # Step 1 — Read keys
    groq_api_key = os.environ.get("GROQ_API_KEY")
    serper_api_key = os.environ.get("SERPER_API_KEY")

    if not groq_api_key:
        raise ValueError("❌ GROQ_API_KEY not found in environment!")
    if not serper_api_key:
        raise ValueError("❌ SERPER_API_KEY not found in environment!")

    # Create Groq LLM
    groq_llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=groq_api_key,
        temperature=0
    )

    # Tool 1 — Python REPL
    python_repl = PythonREPLTool()
    repl_tool = Tool(
        name="python_repl",
        description=(
            "Use this tool to execute Python code for mathematical calculations. "
            "Input must be valid Python code. "
            "Use this for compound interest, growth calculations, or any exact math. "
            "Always print() your final result so it is visible."
        ),
        func=python_repl.run
    )

    # Tool 2 — Serper Search
    serper_search = GoogleSerperAPIWrapper(serper_api_key=serper_api_key)
    search_tool = Tool(
        name="serper_search",
        description=(
            "Use this tool to search the internet for live, real-time financial data. "
            "Use this for current stock prices, index values, exchange rates, or any "
            "live market information that requires up-to-date web facts. "
            "Input should be a clear search query string."
        ),
        func=serper_search.run
    )

    # ReAct Prompt — replaces hub.pull
    react_prompt = PromptTemplate.from_template(
        "Answer the following questions as best you can. "
        "You have access to the following tools:\n\n"
        "{tools}\n\n"
        "Use the following format:\n\n"
        "Question: the input question you must answer\n"
        "Thought: you should always think about what to do\n"
        "Action: the action to take, should be one of [{tool_names}]\n"
        "Action Input: the input to the action\n"
        "Observation: the result of the action\n"
        "... (this Thought/Action/Action Input/Observation can repeat N times)\n"
        "Thought: I now know the final answer\n"
        "Final Answer: the final answer to the original input question\n\n"
        "Begin!\n\n"
        "Question: {input}\n"
        "Thought:{agent_scratchpad}"
    )

    # Step 2 — Smoke tests
    print("=" * 55)
    print("=== Tool Smoke Tests ===")
    print("=" * 55)
    test_tools(repl_tool, search_tool)

    # Step 3 — Python only agent
    print("\n" + "=" * 55)
    print("=== Python-Only Agent ===")
    print("=" * 55)
    run_python_agent(groq_llm, repl_tool, react_prompt)

    # Step 4 — Search + Python agent
    print("\n" + "=" * 55)
    print("=== Two-Tool Search Agent ===")
    print("=" * 55)
    run_search_agent(groq_llm, search_tool, repl_tool, react_prompt)

    print("\n" + "=" * 55)
    print("🎉 FinPulse ReAct Agent — All Steps Complete!")
    print("=" * 55)


if __name__ == "__main__":
    main()