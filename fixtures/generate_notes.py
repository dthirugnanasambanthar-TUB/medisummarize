#pydantic - define the structure of the data in such a way that validation is automatic and easy
from pydantic import BaseModel
from typing import Optional, List
import os
import json
from groq import Groq
from dotenv import load_dotenv

class SOAPGroundTruth(BaseModel):
    subjective: str
    objective: str
    assessment: str
    plan: str

class NoteMetadata(BaseModel):
    age: int
    gender: str
    chief_complaint: str
    has_allergies: bool
    allergies: List[str]

class PatientNote(BaseModel):
    note_id: str
    raw_text: str
    ground_truth: SOAPGroundTruth
    metadata: NoteMetadata

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

CASE_TEMPLATES = [
    {"age_range": "18-30", "gender": "F", "complaint": "appendicitis"},
    {"age_range": "40-55", "gender": "M", "complaint": "type 2 diabetes follow-up"},
    {"age_range": "60-75", "gender": "F", "complaint": "hip fracture"},
    {"age_range": "25-35", "gender": "M", "complaint": "asthma attack"},
    {"age_range": "50-65", "gender": "F", "complaint": "hypertensive crisis"},
    {"age_range": "70-85", "gender": "M", "complaint": "stroke symptoms"},
    {"age_range": "30-45", "gender": "F", "complaint": "urinary tract infection"},
    {"age_range": "45-60", "gender": "M", "complaint": "lower back pain"},
    {"age_range": "20-30", "gender": "F", "complaint": "anxiety attack"},
    {"age_range": "65-80", "gender": "M", "complaint": "COPD exacerbation"},
]

def generate_single_note(note_number: int, template: dict) -> PatientNote:
    prompt = f"""Generate a realistic synthetic patient note for a hospital setting.
        Return ONLY valid JSON. No explanation, no markdown, no code blocks. Just the raw JSON object.

        Patient details you MUST use:
        - Age: pick a specific age within {template['age_range']} years old
        - Gender: {template['gender']}
        - Chief complaint: {template['complaint']}

        The JSON must match this exact structure:
        {{
        "note_id": "note_{note_number:03d}",
        "raw_text": "a messy unstructured note as a doctor would write it, at least 5 sentences",
        "ground_truth": {{
            "subjective": "what the patient reports",
            "objective": "measurable clinical findings",
            "assessment": "doctor's diagnosis or impression",
            "plan": "next steps and treatment"
        }},
        "metadata": {{
            "age": <integer within {template['age_range']}>,
            "gender": "{template['gender']}",
            "chief_complaint": "{template['complaint']}",
            "has_allergies": <true or false>,
            "allergies": ["<allergy1>"] or []
        }}
        }}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )

    raw_output = response.choices[0].message.content.strip()
    data = json.loads(raw_output)
    note = PatientNote(**data)
    note.note_id = f"note_{note_number:03d}"
    return note

if __name__ == "__main__":
    import time
    
    notes = []
    total = 50
    
    for i in range(1, total + 1):
        template = CASE_TEMPLATES[(i - 1) % len(CASE_TEMPLATES)]
        print(f"Generating note {i}/{total} ({template['complaint']})...", end=" ")
        
        try:
            note = generate_single_note(i, template)
            notes.append(note.model_dump())
            print("✓")
        except Exception as e:
            print(f"✗ failed: {e}")
        
        time.sleep(1)
    
    # Save to fixtures folder
    output_path = "fixtures/patient_notes.json"
    with open(output_path, "w") as f:
        json.dump(notes, f, indent=2)
    
    print(f"\nDone. {len(notes)} notes saved to {output_path}")