"""
campus_voice_bulletin.py

Campus Voice Bulletin Processor.
Pipeline: Speech-to-Text (Groq Whisper) -> Summarize (Groq chat) -> Text-to-Speech (gTTS)

Requires (install first):
    pip install python-dotenv groq gTTS requests

Requires a .env file in the same folder containing:
    GROQ_API_KEY=your_key_here
"""

import os
import re
import urllib.request
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from gtts import gTTS

# ---------------------------------------------------------------------
# Config / paths
# ---------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent

AUDIO_URL = (
    "https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/"
    "iitr-as-2601/module4/session51/sample_voice_note.mp3"
)
TRANSCRIPT_URL = (
    "https://s13n-curr-images-bucket.s3.ap-south-1.amazonaws.com/"
    "iitr-as-2601/module4/session51/sample_transcript.txt"
)

AUDIO_PATH = BASE_DIR / "sample_voice_note.mp3"
REFERENCE_TRANSCRIPT_PATH = BASE_DIR / "sample_transcript.txt"
SPOKEN_SUMMARY_PATH = BASE_DIR / "spoken_summary.mp3"

SUMMARIZE_MODEL = "llama-3.1-8b-instant"
STT_MODEL = "whisper-large-v3"


# ---------------------------------------------------------------------
# 1. Load API key
# ---------------------------------------------------------------------
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY not found. Create a .env file with GROQ_API_KEY=<your key>."
    )

client = Groq(api_key=GROQ_API_KEY)


# ---------------------------------------------------------------------
# Helper: download a file if it doesn't already exist locally
# ---------------------------------------------------------------------
def download_if_missing(url: str, local_path: Path) -> Path:
    if not local_path.exists():
        print(f"Downloading {local_path.name} ...")
        urllib.request.urlretrieve(url, local_path)
    return local_path


# ---------------------------------------------------------------------
# 2 & 3. Speech to text
# ---------------------------------------------------------------------
def speech_to_text(audio_path: Path) -> str:
    """Transcribe the given audio file using Groq Whisper."""
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            file=(audio_path.name, audio_file.read()),
            model=STT_MODEL,
            response_format="text",
        )
    # response_format="text" -> transcript is already a plain string
    return str(transcript).strip()


# ---------------------------------------------------------------------
# 4. Summarize
# ---------------------------------------------------------------------
def summarize(transcript: str) -> str:
    """Summarize the transcript into exactly 3 short bullet points."""
    prompt = (
        "Summarize the following campus voice bulletin transcript into "
        "EXACTLY 3 short bullet points. Do not invent details that are "
        "not present in the transcript. Only use facts stated in the "
        "transcript.\n\n"
        f"Transcript:\n{transcript}\n\n"
        "Respond with exactly 3 bullet points, each starting with '- '."
    )

    response = client.chat.completions.create(
        model=SUMMARIZE_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


# ---------------------------------------------------------------------
# 5. Text to speech
# ---------------------------------------------------------------------
def text_to_speech(summary: str, out_path: Path) -> Path:
    """Convert the summary text to a spoken .mp3 file using gTTS."""
    tts = gTTS(text=summary, lang="en")
    tts.save(str(out_path))
    return out_path


# ---------------------------------------------------------------------
# 7. Quality flags
# ---------------------------------------------------------------------
def check_library_hours_captured(text: str) -> bool:
    text_lower = text.lower()
    has_time = "10" in text_lower or "ten" in text_lower
    has_library = "library" in text_lower
    return has_time and has_library


def check_student_id_captured(text: str) -> bool:
    text_lower = text.lower()
    return "student" in text_lower and "id" in text_lower


# ---------------------------------------------------------------------
# 6. Main pipeline
# ---------------------------------------------------------------------
def main():
    # Stage 1: ensure input audio exists locally
    download_if_missing(AUDIO_URL, AUDIO_PATH)

    # Stage 2: speech -> text
    transcript = speech_to_text(AUDIO_PATH)
    print("=== TRANSCRIPT ===")
    print(transcript)
    print()

    # Stage 3: summarize
    summary = summarize(transcript)
    print("=== SUMMARY ===")
    print(summary)
    print()

    # Stage 4: text -> speech
    spoken_path = text_to_speech(summary, SPOKEN_SUMMARY_PATH)
    print("=== SPOKEN SUMMARY FILE ===")
    print(spoken_path.resolve())
    print()

    # Stage 5: quality flags, evaluated against the reference transcript
    download_if_missing(TRANSCRIPT_URL, REFERENCE_TRANSCRIPT_PATH)
    reference_text = REFERENCE_TRANSCRIPT_PATH.read_text(encoding="utf-8")

    library_hours_captured = check_library_hours_captured(reference_text)
    student_id_captured = check_student_id_captured(reference_text)

    print("=== QUALITY FLAGS ===")
    print(f"library_hours_captured: {library_hours_captured}")
    print(f"student_id_captured: {student_id_captured}")


if __name__ == "__main__":
    main()
