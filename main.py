from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API key correctly
import os

genai.configure(api_key=os.getenv("AIzaSyDMHOrPaMXph5nrwBmmlXOkA0f-_lvBvus"))

model = genai.GenerativeModel("gemini-1.5-flash")


@app.get("/")
def home():
    return {"message": "Backend is running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    image_bytes = await file.read()

    prompt = """
    Analyze this face and give:
    - Foundation shade
    - Lipstick color
    - Blush color
    - Eye makeup
    - Compliment
    """

    response = model.generate_content([
        prompt,
        {
            "mime_type": file.content_type,
            "data": image_bytes
        }
    ])

    return {"result": response.text}