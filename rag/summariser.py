import os
import json
from groq import Groq
from dotenv import load_dotenv
from pydantic import BaseModel
from store import get_chunks_by_note_id

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class SOAPSummary(BaseModel):
    subjective: str
    objective: str
    assessment: str
    plan: str
    
    
def summarise_note(note_id: str) -> SOAPSummary:
    # Step 1: fetch all chunks for this note
    chunks = get_chunks_by_note_id(note_id)
    
    if not chunks:
        raise ValueError(f"No chunks found for {note_id}")
    
    # Step 2: assemble into readable context
    context = "\n\n".join(chunks)
    
    # Step 3: build the prompt
    system_prompt = """You are a clinical assistant helping doctors review patient notes.
    Your job is to extract a structured SOAP summary from the provided clinical text.

    Rules:
    - Only use information present in the provided text. Never invent facts.
    - Be concise but complete.
    - Return ONLY valid JSON. No explanation, no markdown, no code blocks.

    The JSON must match exactly:
    {
        "subjective": "what the patient reports in their own words",
        "objective": "measurable clinical findings, vitals, test results",
        "assessment": "doctor's diagnosis or clinical impression",
        "plan": "next steps, treatments, referrals, follow-up"
    }"""

    user_message = f"""Please extract a SOAP summary from this patient note: {context}"""

    # Step 4: call Groq
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.1
    )
    
    # Step 5: parse and validate
    raw_output = response.choices[0].message.content.strip()
    data = json.loads(raw_output)
    return SOAPSummary(**data)

if __name__ == "__main__":
    summary = summarise_note("note_001")
    print(summary.model_dump_json(indent=2))