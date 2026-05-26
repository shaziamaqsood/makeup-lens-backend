from fastapi import FastAPI, UploadFile, File
from PIL import Image
import numpy as np
import cv2
import mediapipe as mp
import google.generativeai as genai
from dotenv import load_dotenv
import os
import io

load_dotenv()

app = FastAPI()

genai.configure(api_key=os.getenv("AIzaSyDMHOrPaMXph5nrwBmmlXOkA0f-_lvBvus"))

model = genai.GenerativeModel("gemini-1.5-flash")

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1
)

@app.get("/")
def home():
    return {"message": "Makeup Lens AI Backend Running"}

@app.post("/analyze")
async def analyze_face(file: UploadFile = File(...)):

    contents = await file.read()

    image = Image.open(io.BytesIO(contents)).convert("RGB")
    image_np = np.array(image)

    results = face_mesh.process(image_np)

    if not results.multi_face_landmarks:
        return {"error": "No face detected"}

    # ---------- Skin Tone Detection ----------
    h, w, _ = image_np.shape

    center_x = w // 2
    center_y = h // 2

    skin_pixel = image_np[center_y, center_x]

    r, g, b = skin_pixel

    skin_description = f"""
    RGB skin tone values:
    R={r}
    G={g}
    B={b}
    """

    # ---------- AI Recommendation ----------
    prompt = f"""
    You are a professional makeup artist AI.

    Analyze this skin tone:
    {skin_description}

    Generate:
    1. Foundation shade
    2. Powder tone
    3. Blush color
    4. Lipstick color
    5. Eye makeup recommendation

    Generate fresh intelligent recommendations.
    Do NOT use fixed values.
    """

    response = model.generate_content(prompt)

    return {
        "recommendations": response.text
    }