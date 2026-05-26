from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import google.generativeai as genai
import os
import io
from PIL import Image


app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


@app.get("/")
def home():
    return {"message": "Makeup Lens API Running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    image_bytes = await file.read()

    image = Image.open(io.BytesIO(image_bytes))

    prompt = """
    You are a professional makeup artist AI.

    Analyze the face image and provide:
    1. Foundation recommendation
    2. Powder recommendation
    3. Blush recommendation
    4. Lipstick recommendation
    5. Eye makeup recommendation
    6. Beauty compliment

    Make it personalized and real-time.
    """

    response = model.generate_content([
        prompt,
        image
    ])

    return {
        "recommendations": response.text
    }