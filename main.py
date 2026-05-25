from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from models.face_model import FaceModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Face model
face_model = FaceModel()


# ---------------- FACE ANALYSIS ---------------- #
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        img_bytes = await file.read()

        np_arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        result = face_model.analyze(img)

        return {
            "success": True,
            "analysis": result
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }