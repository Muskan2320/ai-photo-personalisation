from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageDraw
from fastapi.staticfiles import StaticFiles
import cv2
import numpy as np
import uuid
import os

app = FastAPI()

app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def cartoonize_face(face):
    # Convert to grayscale
    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 7)

    # Detect edges
    edges = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        9, 9
    )

    # Smooth colors
    color = cv2.bilateralFilter(face, 9, 250, 250)

    # Combine edges and color
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon

@app.post("/generate")
async def generate_image(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())

    input_path = f"{UPLOAD_DIR}/{file_id}.png"
    output_path = f"{OUTPUT_DIR}/{file_id}_final.png"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Load uploaded image
    image = cv2.imread(input_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Face detection
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    h_img, w_img, _ = image.shape

    if len(faces) == 0:
        # Center crop fallback
        cx, cy = w_img // 2, h_img // 2
        crop_size = min(w_img, h_img) // 3
        x = max(cx - crop_size // 2, 0)
        y = max(cy - crop_size // 2, 0)
        face = image[y:y+crop_size, x:x+crop_size]
    else:
        x, y, w, h = faces[0]
        face = image[y:y+h, x:x+w]

    # Cartoonize face
    face = cartoonize_face(face)

    # Convert face to PIL
    face_img = Image.fromarray(
        cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    ).convert("RGBA")

    face_img = face_img.resize((200, 200))

    # Load base illustration
    base = Image.open("../assets/base_illustration.png").convert("RGBA")

    # Create circular mask
    mask = Image.new("L", face_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 200, 200), fill=255)

    face_img.putalpha(mask)

    # Paste face onto illustration
    base.paste(face_img, (250, 150), face_img)

    # Save output
    base.save(output_path)

    return {"image_path": output_path}
