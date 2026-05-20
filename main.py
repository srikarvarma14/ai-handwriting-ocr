from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pytesseract
import io
import cv2
import numpy as np

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
@app.get("/")
async def home():
    return FileResponse("index.html")

# OCR endpoint
@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))

        # Convert to grayscale
        gray = image.convert("L")
        image_np = np.array(gray)

        # Improve dark images
        if np.mean(image_np) < 127:
            image_np = cv2.bitwise_not(image_np)

        # Threshold
        _, thresh = cv2.threshold(
            image_np,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        # OCR
        text = pytesseract.image_to_string(
            thresh,
            config='--oem 3 --psm 6'
        )

        if not text.strip():
            return JSONResponse(
                {"error": "No text found in image"},
                status_code=400
            )

        return JSONResponse({"text": text})

    except Exception as e:
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )