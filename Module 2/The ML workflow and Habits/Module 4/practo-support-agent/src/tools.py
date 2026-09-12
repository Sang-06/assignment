import json
import os
from typing import Dict, Any, Optional

class AgentTools:
    @staticmethod
    def calculate_escalation_score(follow_up_required: bool, days_since_created: int) -> Dict[str, Any]:
        """
        Calculates escalation score using the exact formula:
        Escalation Score = 0.6 * follow_up_required + 0.4 * (days_since_created / 30)
        """
        esc_score = (0.6 * (1.0 if follow_up_required else 0.0)) + (0.4 * (days_since_created / 30.0))
        esc_score = round(esc_score, 4)
        needs_escalation = esc_score >= 0.65
        return {
            "escalation_score": esc_score,
            "needs_escalation": needs_escalation
        }

    @staticmethod
    def check_appointment_status(record_id: Optional[str] = None, appointment_id: Optional[str] = None, data_path: str = "data/appointments.json") -> Dict[str, Any]:
        """
        Looks up appointment record by ID (accepts either record_id or appointment_id keyword).
        """
        target_id = record_id or appointment_id
        if not target_id:
            return {"found": False, "error": "No appointment ID provided."}

        if not os.path.exists(data_path):
            return {"found": False, "error": "Database file missing."}
            
        with open(data_path, "r", encoding="utf-8") as f:
            records = json.load(f)
            
        for rec in records:
            if rec["record_id"].strip().upper() == target_id.strip().upper():
                days = rec["days_since_created"]
                follow_up = rec["follow_up_required"]
                
                esc_data = AgentTools.calculate_escalation_score(follow_up, days)
                
                return {
                    "found": True,
                    "record_id": rec["record_id"],
                    "status": rec["status"],
                    "category": rec["category"],
                    "consultation_fee_inr": rec["consultation_fee_inr"],
                    "days_since_created": days,
                    "follow_up_required": follow_up,
                    "escalation_score": esc_data["escalation_score"],
                    "needs_escalation": esc_data["needs_escalation"]
                }
                
        return {"found": False, "message": f"Record {target_id} not found."}

    # Aliases for MCP server compatibility
    lookup_appointment_status = check_appointment_status