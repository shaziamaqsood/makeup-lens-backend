from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import os, io, json
import numpy as np
import cv2
from PIL import Image
from ai_pipeline import enhance

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
    return {"message": "Makeup Lens API Running"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    np_img = np.array(image)
    cv_img = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)

    # STEP 1: Enhance face
    enhanced = enhance(cv_img)

    cv2.imwrite("result.jpg", enhanced)

    # STEP 2: Gemini prompt
    prompt = """
Return ONLY JSON makeup analysis:
{
 "foundation":"",
 "powder":"",
 "blush":"",
 "lipstick":"",
 "eye_makeup":"",
 "compliment":"",
 "recommendation_summary":""
}
"""

    response = client.models.generate_content(
        model="gemini-1.5-flash-002",
        contents=[prompt, image]
    )

    text = response.text.replace("```json", "").replace("```", "")

    try:
        result = json.loads(text)
    except:
        result = {"error": "invalid json", "raw": text}

    return {
        "analysis": result,
        "image_url": "/result.jpg"
    }