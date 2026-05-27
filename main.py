from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import os
import io
from PIL import Image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.get("/")
def home():
    return {"message": "Makeup Lens API Running 🚀"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    prompt = """
You are a professional AI makeup expert.

Analyze face deeply and return ONLY JSON:

{
  "foundation": "",
  "powder": "",
  "blush": "",
  "lipstick": "",
  "eye_makeup": "",
  "compliment": "",
  "recommendation_summary": ""
}

Rules:
- fully personalized
- no templates
- no static values
"""

    response = client.models.generate_content(
        model="gemini-1.5-pro-vision",
        contents=[prompt, image]
    )

    return {"result": response.text}