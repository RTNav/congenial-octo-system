import openai
import os
import json
import random
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or use your Vercel domain instead of "*" for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# debug environment key
print("OpenAI key loaded:", openai.api_key[:5] + "..." if openai.api_key else "None")

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
    try:
        if req.direct_lyrics:
            candidates = [l for l in labeled_lyrics if l["mood"].lower() in tone_map.get(req.tone.lower(), [])]
            if not candidates:
                candidates = labeled_lyrics
            lyric = random.choice(candidates)
            return {"reply": f"\"{lyric['line']}\" — {lyric['song']}"}
        else:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a poetic, slightly cryptic assistant who always sounds like a "
                            "Twenty One Pilots lyricist. Respond in one or two lines of poetic, emotional text."
                        )
                    },
                    {"role": "user", "content": req.prompt}
                ],
                temperature=0.8
            )
            reply = response.choices[0].message["content"].strip()
            return {"reply": reply}
    except Exception as e:
        print("ERROR:", e)
        return {"reply": "Sorry, something went wrong. Like in life."}
