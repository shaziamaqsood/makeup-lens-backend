from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os
from google import genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    return genai.Client(api_key=api_key)


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    client = get_client()

    if client is None:
        return {"error": "API key missing on server"}

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
            {
                "inline_data": {
                    "mime_type": file.content_type,
                    "data": image_bytes
                }
            }
        ]
    )

    return {"result": response.text}