import json
import random
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or use your Vercel domain instead of "*" for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    prompt: str
    direct_lyrics: bool = True
    tone: str = "cryptic"

# Load labeled lyrics
with open("lyrics_labeled.json", "r", encoding="utf-8") as f:
    labeled_lyrics = json.load(f)

# Tone category mapping
tone_map = {
    "cryptic": ["cryptic", "philosophical", "abstract"],
    "hopeful": ["hopeful", "resilient", "inspirational"],
    "dark": ["dark", "anxious", "melancholy"],
    "chaotic": ["chaotic", "rebellious", "confused"],
    "philosophical": ["philosophical", "reflective", "introspective"]
}

@app.post("/chat")
def chat(req: RequestData):
    if req.direct_lyrics:
        candidates = [l for l in labeled_lyrics if l["mood"].lower() in tone_map.get(req.tone.lower(), [])]
        if not candidates:
            candidates = labeled_lyrics
        lyric = random.choice(candidates)
        return {"reply": f"\"{lyric['line']}\" — {lyric['song']}"}
    else:
        return {"reply": f"(Non-lyric mode not yet implemented)"}
