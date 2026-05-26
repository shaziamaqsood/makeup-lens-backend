from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os

from google import genai
from google.genai import types

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ CORRECT: use environment variable name
client = genai.Client(api_key=os.getenv("AIzaSyDMHOrPaMXph5nrwBmmlXOkA0f-_lvBvus"))


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    image_bytes = await file.read()

    prompt = """
    Analyze this face image and give:
    1. Makeup recommendation
    2. Compliment
    3. Suggested style
    Return JSON format.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            prompt,
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=file.content_type
            )
        ]
    )

    return {
        "result": response.text
    }