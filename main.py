from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import google.generativeai as genai
import os
import io
from PIL import Image

# ----------------------------
# CREATE APP
# ----------------------------
app = FastAPI()

# ----------------------------
# CORS
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# STATIC FOLDER
# ----------------------------
if not os.path.exists("outputs"):
    os.makedirs("outputs")

app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# ----------------------------
# GEMINI CONFIG
# ----------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise Exception("GEMINI_API_KEY is missing in environment variables")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash-001")

# ----------------------------
# ROUTES
# ----------------------------
@app.get("/")
def home():
    return {"message": "Makeup Lens API Running 🚀"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()

        # IMPORTANT FIX
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

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

        response = model.generate_content([prompt, image])

        return {
            "recommendations": response.text
        }

    except Exception as e:
        return {
            "error": str(e)
        }