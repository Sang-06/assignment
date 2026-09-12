from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, START, END

from src.guardrails import GuardrailEngine
from src.tools import AgentTools
from src.vectorstore import VectorStoreManager
from src.mock_llm import MockLLM

class AgentState(TypedDict):
    query: str
    appointment_id: Optional[str]
    masked_query: str
    is_injection: bool
    route: str
    appointment_data: Optional[Dict[str, Any]]
    retrieved_chunks: List[Dict]
    escalation_info: Dict[str, Any]
    final_response: str
    sources: List[str]

class PractoLangGraphAgent:
    def __init__(self):
        self.vsm = VectorStoreManager(collection_name="practo_fixed")
        self.vsm.ingesting_kb(strategy="fixed_size")
        self.graph = self._build_graph()

    def guardrail_node(self, state: AgentState) -> AgentState:
        query = state.get("query", "")
        if GuardrailEngine.detect_prompt_injection(query):
            state["is_injection"] = True
            state["final_response"] = "Security Warning: Prompt injection attempt detected. Request blocked."
        else:
            state["is_injection"] = False
            state["masked_query"] = GuardrailEngine.mask_pii(query)
        return state

    def appointment_lookup_node(self, state: AgentState) -> AgentState:
        app_id = state.get("appointment_id")
        if app_id:
            lookup = AgentTools.check_appointment_status(app_id)
            state["appointment_data"] = lookup
        else:
            state["appointment_data"] = None
        return state

    def rag_retrieval_node(self, state: AgentState) -> AgentState:
        masked = state.get("masked_query", state.get("query", ""))
        chunks = self.vsm.query_kb(masked, top_k=3)
        state["retrieved_chunks"] = chunks
        return state

    def generation_node(self, state: AgentState) -> AgentState:
        chunks = state.get("retrieved_chunks", [])
        query_str = state.get("masked_query", state.get("query", ""))
        llm_out = MockLLM.generate_grounded_response(query_str, chunks)
        
        response_text = llm_out["response"]
        sources = llm_out.get("sources", [])
        
        # Append appointment details if lookup was performed
        app_data = state.get("appointment_data")
        if app_data and app_data.get("found"):
            esc_msg = f" (Escalation Score: {app_data['escalation_score']})" if app_data.get("needs_escalation") else ""
            response_text += f"\n\n[Appointment {app_data['record_id']} Status: {app_data['status']}{esc_msg}]"
            sources.append("appointments.json")
            
        state["final_response"] = response_text
        state["sources"] = sources
        return state

    def _select_route(self, state: AgentState) -> str:
        if state.get("is_injection"):
            return "end"
        return "continue"

    def _build_graph(self):
        builder = StateGraph(AgentState)
        
        builder.add_node("guardrail", self.guardrail_node)
        builder.add_node("appointment_lookup", self.appointment_lookup_node)
        builder.add_node("rag_retrieval", self.rag_retrieval_node)
        builder.add_node("generation", self.generation_node)
        
        builder.set_entry_point("guardrail")
        
        builder.add_conditional_edges(
            "guardrail",
            self._select_route,
            {
                "continue": "appointment_lookup",
                "end": END
            }
        )
        
        builder.add_edge("appointment_lookup", "rag_retrieval")
        builder.add_edge("rag_retrieval", "generation")
        builder.add_edge("generation", END)
        
        return builder.compile()

    def run(self, query: str, appointment_id: Optional[str] = None) -> Dict[str, Any]:
        initial_state: AgentState = {
            "query": query,
            "appointment_id": appointment_id,
            "masked_query": query,
            "is_injection": False,
            "route": "rag",
            "appointment_data": None,
            "retrieved_chunks": [],
            "escalation_info": {},
            "final_response": "",
            "sources": []
        }
        return self.graph.invoke(initial_state)