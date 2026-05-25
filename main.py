from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini API Key
genai.configure(api_key=os.getenv("AIzaSyA8Qj4tagNKWp_AEN6Ioep6Q040N-vd-Dw"))

model = genai.GenerativeModel("gemini-1.5-flash")


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    image_bytes = await file.read()

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    prompt = """
    Analyze this face image and give:
    1. Makeup recommendation
    2. Compliment
    3. Suggested style
    Return in JSON format:
    {
      "recommendation": "",
      "compliment": "",
      "output_image": ""
    }
    """

    response = model.generate_content([
        prompt,
        {"mime_type": file.content_type, "data": image_bytes}
    ])

    return {
        "result": response.text
    }