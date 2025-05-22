from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import random
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

with open("lyrics_data.json") as f:
    lyrics_db = json.load(f)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    direct_lyrics = data.get("direct_lyrics", True)
    tone = data.get("tone", "cryptic")

    if direct_lyrics:
        matching_lyrics = [l for l in lyrics_db if l["mood"] == tone] or lyrics_db
        lyric = random.choice(matching_lyrics)["line"]
        reply = f"\"{lyric}\" — Twenty One Pilots"
    else:
        gpt_prompt = f"Respond in a {tone} tone using the style of a Twenty One Pilots lyric: {prompt}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": gpt_prompt}]
        )
        reply = response.choices[0].message.content.strip()

    return { "reply": reply }
