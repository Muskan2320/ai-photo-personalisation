
# AI Photo Personalisation Prototype

This project is a small end-to-end prototype that demonstrates how a child’s photo can be used to personalise a storybook illustration. The goal is to showcase AI-driven personalisation, full-stack integration, and practical engineering trade-offs using free and lightweight tools.

---

## 🧠 Overview

The system allows a user to:
1. Upload a child’s photo via a React frontend
2. Process the image in a FastAPI backend
3. Extract and stylise the child’s face
4. Insert the stylised face into a predefined storybook illustration
5. Return a personalised illustration to the user

This mirrors how personalised children’s books are created using illustration templates and child-specific visual features.

---

## 🏗️ Architecture

[ React Frontend (Vercel) ]  
        ↓  
[ FastAPI Backend (GitHub Codespaces) ]  
        ↓  
[ Face Detection (OpenCV) ]  
        ↓  
[ Face Stylisation (Cartoon Filter) ]  
        ↓  
[ Base Illustration Template ]  
        ↓  
[ Personalised Illustration Output ]  

---

## 🛠️ Tech Stack

### Frontend
- React (Vite)
- Deployed on Vercel (Free tier)

### Backend
- Python
- FastAPI
- OpenCV (headless)
- Pillow (image processing)
- Deployed via GitHub Codespaces

---

## 🤖 AI Personalisation Pipeline

### 1. Face Detection
OpenCV’s Haar Cascade is used to detect the child’s face. If detection fails (e.g., stylised or low-quality images), a center-crop fallback is applied to keep the pipeline robust.

### 2. Face Stylisation
A lightweight cartoonisation filter (bilateral filtering + edge detection) is applied to the extracted face to better match the illustration style.

### 3. Image Compositing
The stylised face is resized, masked with a circular alpha mask, and blended into a predefined storybook illustration template.

---

## 🎨 Why a Base Illustration Template?

The prototype uses a static base illustration to represent an existing storybook page. In real-world personalised book systems, illustrations are typically hand-drawn by artists and reused as templates, with only character faces being personalised per child.

---

## 📌 Model & Design Choices

- **Why not diffusion models (SDXL / InstantID)?**  
  These models require GPU infrastructure and paid services. For this assignment, the focus was on demonstrating the personalisation pipeline using free, CPU-friendly tools.

- **Why OpenCV + classical image processing?**  
  They are lightweight, fast to prototype, and suitable for demonstrating engineering logic and system design without external dependencies.

---

## ⚠️ Limitations

- Identity preservation is approximate
- Face alignment and positioning are heuristic-based
- Only one illustration template is used
- Lighting and color mismatch may occur

---

## 🚀 Future Improvements (v2)

- Replace cartoonisation + compositing with identity-preserving diffusion models (e.g., InstantID + SDXL)
- Support multiple illustration templates
- Automatic face alignment using facial landmarks
- Add child safety checks and moderation
- Batch generation for full storybooks

---

## ✅ Status

This prototype demonstrates a complete, end-to-end AI personalisation system using free resources, with clear scope for production-grade improvements.
