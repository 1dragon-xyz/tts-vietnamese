from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import edge_tts
import os

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TTSRequest(BaseModel):
    text: str
    voice: str

# Define supported voices
SUPPORTED_VOICES = [
    {"ShortName": "vi-VN-HoaiMyNeural", "FriendlyName": "Vietnamese (Female)", "Gender": "Female", "Locale": "vi-VN"},
    {"ShortName": "vi-VN-NamMinhNeural", "FriendlyName": "Vietnamese (Male)", "Gender": "Male", "Locale": "vi-VN"},
    {"ShortName": "en-US-AvaNeural", "FriendlyName": "English (Female)", "Gender": "Female", "Locale": "en-US"},
    {"ShortName": "en-US-AndrewNeural", "FriendlyName": "English (Male)", "Gender": "Male", "Locale": "en-US"},
    {"ShortName": "zh-CN-XiaoxiaoNeural", "FriendlyName": "Chinese (Female)", "Gender": "Female", "Locale": "zh-CN"},
    {"ShortName": "zh-CN-YunxiNeural", "FriendlyName": "Chinese (Male)", "Gender": "Male", "Locale": "zh-CN"},
    {"ShortName": "ja-JP-NanamiNeural", "FriendlyName": "Japanese (Female)", "Gender": "Female", "Locale": "ja-JP"},
    {"ShortName": "ja-JP-KeitaNeural", "FriendlyName": "Japanese (Male)", "Gender": "Male", "Locale": "ja-JP"},
]

@app.get("/api/voices")
async def get_voices():
    return SUPPORTED_VOICES

@app.post("/api/tts")
async def text_to_speech(request: TTSRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        communicate = edge_tts.Communicate(request.text, request.voice)
        audio_data = b""
        
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        return Response(content=audio_data, media_type="audio/mpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve static files (HTML/CSS/JS) for local development
# Vercel handles this via vercel.json in production, but this allows running locally with 'uvicorn'
public_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "public")
if os.path.exists(public_path):
    app.mount("/", StaticFiles(directory=public_path, html=True), name="public")
