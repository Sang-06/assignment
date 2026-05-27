import os
from datetime import datetime
import requests

# --- Set your model names --
LOCAL_MODEL = "qwen2.5:0.5b"          # 0.5B or 1B only; must match `ollama list`
GROQ_MODEL  = "llama-3.3-70b-versatile"  # check console.groq.com for available models

CANDIDATE = {
    "name":       "Aarav Mehta",
    "email":      "aarav.mehta@example.com",
    "phone":      "+91-98765-43210",
    "location":   "Roorkee, Uttarakhand",
    "education":  "B.Tech Computer Science, IIT Roorkee (expected 2026), CGPA 8.4",
    "skills":     ["Python", "REST APIs", "SQL", "Git", "Basic ML"],
    "experience": "Summer intern at TechBridge Labs (Jun-Aug 2025): built internal dashboards with FastAPI and PostgreSQL.",
    "projects":   "Hostel Room Booking CLI (Python) — 200+ active users on campus.",
}

RESUME_PROMPT = f"""You are a professional resume writer. Create a complete, single-page resume in valid HTML only.
 
Rules:
- Return ONLY HTML starting with <!DOCTYPE html> — no markdown fences, no explanation before or after.
- Do not invent employers, degrees, or facts not listed below.
 
Layout (required):
- Use a **two-column** layout for the main body (e.g. CSS flexbox or CSS grid with two columns).
- **Left column (narrower, ~30-35%):** contact block, Skills, Education.
- **Right column (wider, ~65-70%):** Experience, Projects.
- **Full-width header** above the columns: candidate name (large), one-line title or tagline, email / phone / location on one line.
 
Styling (use a <style> block in <head> — make it look polished):
- Font: a clean sans-serif stack (e.g. Arial, Helvetica, or system-ui).
- **Accent color:** one professional color (e.g. #2563eb blue or #0f766e teal) for headings, section titles, and subtle borders.
- Section headings: uppercase or small-caps, accent color, bottom border or left border.
- Consistent spacing: padding inside columns, margin between sections, readable line-height (1.4-1.6).
- Skills: show as a neat list or small pill/tag style — not a plain comma-separated paragraph.
- Page: max-width ~900px, centered on screen; light background (#f8fafc) with white column areas or a white card look.
- Print-friendly: avoid horizontal scroll; keep everything on one screen-height page if possible.

Candidate data:
Name: {CANDIDATE['name']}
Email: {CANDIDATE['email']}
Phone: {CANDIDATE['phone']}
Location: {CANDIDATE['location']}
Education: {CANDIDATE['education']}
Skills: {', '.join(CANDIDATE['skills'])}
Experience: {CANDIDATE['experience']}
Projects: {CANDIDATE['projects']}
"""
 
 
def save_resume_html(html_text: str, mode: str) -> str:
    """
    Save model output to an HTML file. USE THIS FUNCTION AS-IS — do not change the logic.
 
    File name pattern:
      Local  -> Local_Resume_YYYYMMDD_HHMMSS.html
      Groq   -> Groq_Resume_YYYYMMDD_HHMMSS.html
    """
    prefix   = "Local" if mode == "local" else "Groq"
    stamp    = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_Resume_{stamp}.html"
 
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_text)
 
    print(f"Saved {filename}")
    return filename
 
 
def ask_llm(mode: str, prompt_text: str) -> str:
    """
    Calls the appropriate LLM based on mode.
 
    mode "local":
        Sends request to Ollama running locally on port 11434.
        No API key needed.
 
    mode "groq":
        Reads GROQ_API_KEY from environment variable.
        Uses the Groq Python SDK to call the large model.
    """
 
    if mode == "local":
        # ── LOCAL: Ollama REST API ──────────────────────────────────────
        url  = "http://localhost:11434/api/chat"
        body = {
            "model":    LOCAL_MODEL,
            "messages": [{"role": "user", "content": prompt_text}],
            "stream":   False,
        }
        response = requests.post(url, json=body, timeout=300)
        response.raise_for_status()
        return response.json()["message"]["content"]
 
    elif mode == "groq":
        # ── GROQ: Groq Python SDK ───────────────────────────────────────
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable is not set. "
                "Export it with: export GROQ_API_KEY='your-key-here'"
            )
 
        from groq import Groq
        client   = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt_text}],
        )
        return response.choices[0].message.content
 
    else:
        raise ValueError(f"Unknown mode '{mode}'. Use 'local' or 'groq'.")
 
 
def generate_resume_html(mode: str) -> str:
    """Call the LLM, then save HTML using save_resume_html (do not change this function)."""
    html_from_model = ask_llm(mode, RESUME_PROMPT)
    return save_resume_html(html_from_model, mode)
 
 
if __name__ == "__main__":
    print("Generating local resume...")
    generate_resume_html("local")
 
    print("Generating Groq resume...")
    try:
        generate_resume_html("groq")
    except ValueError as e:
        print(f"Groq skipped: {e}")
 
    print("Open both HTML files in your browser and compare quality.")
 
# TODO after comparing both files in the browser — replace the lines below (2 lines; mention styling):
# Local resume quality: Basic but functional. The qwen2.5:0.5b model produced valid HTML with a two-column layout, however the styling was minimal — plain fonts, no accent colors, skills shown as a simple list, and inconsistent spacing. The resume was readable but lacked visual polish.
# Groq resume quality: Significantly better. The llama-3.3-70b-versatile model produced a well-structured, visually polished resume with a clean two-column layout, teal/blue accent colors on headings, skill pills/tags, proper section borders, consistent padding, and a professional card-style design — clearly submission-ready.

# Local resume quality: Poor. The qwen2.5:0.5b model returned markdown fences (```html) making the file fail to open in the browser. The HTML itself was incomplete — no two-column layout, missing Education and Projects sections, prompt instructions leaked into the footer, and overall minimal styling with no skill tags or proper structure.
# Groq resume quality: Excellent. The llama-3.3-70b-versatile model produced valid, well-structured HTML with a proper two-column layout, teal accent colors, skill pills, all required sections (Education, Experience, Projects), consistent spacing, and a polished professional design — fully renderable in the browser.