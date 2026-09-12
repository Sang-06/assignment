import json
import os
import random
from typing import List, Dict
from pydantic import BaseModel, Field

class AppointmentRecord(BaseModel):
    record_id: str
    category: str
    status: str
    consultation_fee_inr: float = Field(..., ge=500, le=1500)
    days_since_created: int = Field(..., ge=0, le=30)
    follow_up_required: bool

CATEGORIES = ["General Medicine", "Cardiology", "Dermatology", "Pediatrics", "Orthopedics"]
STATUSES = ["Scheduled", "Completed", "Cancelled", "No-Show", "Rescheduled"]

# Renamed function to match test suite import expectation
def generate_appointment_dataset(seed: int = 42, num_records: int = 44, output_path: str = "data/appointments.json") -> List[Dict]:
    random.seed(seed)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    records = []
    for i in range(num_records):
        category = CATEGORIES[i % len(CATEGORIES)]
        status = STATUSES[i % len(STATUSES)]
        
        base_fee = 500.0 if category in ["General Medicine", "Pediatrics"] else 900.0
        fee = base_fee + random.randint(0, 6) * 100.0
        days_since = random.randint(0, 30)
        follow_up = random.random() < 0.20
        
        rec = AppointmentRecord(
            record_id=f"APP-{1000 + i}",
            category=category,
            status=status,
            consultation_fee_inr=fee,
            days_since_created=days_since,
            follow_up_required=follow_up
        )
        records.append(rec.model_dump())

    follow_up_count = sum(1 for r in records if r["follow_up_required"])
    follow_up_pct = (follow_up_count / len(records)) * 100
    assert 10.0 <= follow_up_pct <= 30.0, f"Follow up % ({follow_up_pct:.1f}%) out of bounds!"
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
        
    print(f"✅ Generated {len(records)} records. Follow-up rate: {follow_up_pct:.1f}% ({follow_up_count}/{len(records)})")
    return records

def generate_kb_documents(kb_dir: str = "data/kb_documents"):
    os.makedirs(kb_dir, exist_ok=True)
    kb_topics = [
        ("appointment_booking_policy.txt", "Practo Appointment Booking Policy:\nPatients can book clinic appointments up to 30 days in advance via the Practo portal. Confirmation is sent instantly upon selecting an available slot. A valid 10-digit phone number is required for all bookings."),
        ("cancellation_rescheduling_window.txt", "Cancellation and Rescheduling Window:\nFree cancellation and slot rescheduling are permitted up to 2 hours prior to the scheduled consultation. Cancellations within 2 hours incur a 50% fee deduction. No-show appointments receive zero refund."),
        ("consultation_fee_structure.txt", "Consultation Fee Structure by Specialty:\nGeneral Medicine and Pediatrics consultation fees range between 500 and 800 INR. Specialized consultations for Cardiology, Orthopedics, and Dermatology range between 900 and 1500 INR."),
        ("insurance_claim_process.txt", "Insurance Claim Process:\nPatients can download itemized consultation bills and diagnostic summaries directly from the app. Cashless claims are supported at network hospitals upon presenting a valid digital insurance ID."),
        ("prescription_refill_policy.txt", "Prescription Refill Policy:\nPrescription refills for chronic conditions can be requested online within 90 days of the last doctor visit. Approvals require doctor verification and a digital signature before pharmacy dispatch."),
        ("lab_test_turnaround.txt", "Lab Test Turnaround Times:\nStandard blood work and routine lab test reports are published within 12 to 24 hours. Specialized pathology and culture reports require up to 48 to 72 hours for complete verification."),
        ("telemedicine_eligibility.txt", "Telemedicine Eligibility:\nVideo consultations are eligible for non-emergency follow-ups, minor symptoms, and routine medication renewals. Life-threatening conditions and severe trauma are strictly ineligible for teleconsultation."),
        ("emergency_visit_protocol.txt", "Emergency Visit Protocol:\nPracto support channels do not handle acute medical emergencies. Patients experiencing severe chest pain, major bleeding, or respiratory distress must immediately call emergency services (108) or visit the nearest ER."),
        ("patient_data_privacy.txt", "Patient Data Privacy Policy:\nAll health records and personal consultation data are encrypted using 256-bit encryption standard. Contact phone numbers and personal identifiers are sanitized to ensure strict privacy compliance."),
        ("follow_up_visit_discount.txt", "Follow-up Visit Discount Policy:\nFollow-up consultations scheduled within 7 days of the primary visit receive a 50% discount on standard consultation fees. Full standard rates apply after 7 days."),
        ("second_opinion_process.txt", "Second Opinion Process:\nPatients seeking a second medical opinion can securely upload existing medical records and lab results. A senior medical specialist reviews the file and issues a detailed formal assessment within 24 hours."),
        ("home_visit_eligibility.txt", "Home Visit Eligibility:\nDoctor home visits are available exclusively for elderly, post-surgery, or mobility-impaired patients residing in designated metropolitan areas. Bookings must be placed at least 24 hours in advance.")
    ]
    for filename, content in kb_topics:
        with open(os.path.join(kb_dir, filename), "w", encoding="utf-8") as f:
            f.write(content)
    print(f"✅ Generated {len(kb_topics)} KB documents in {kb_dir}")

if __name__ == "__main__":
    generate_appointment_dataset()
    generate_kb_documents()
