from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import json

from video_processor import extract_frames
from pose_analyzer import analyze_frames
from scoring import analyze_score


app = FastAPI(title="MohanLean API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/results", StaticFiles(directory="results"), name="results")

os.makedirs("results", exist_ok=True)

app.mount(
    "/results",
    StaticFiles(directory="results"),
    name="results"
)


@app.get("/")
def home():
    return {
        "message": "MohanLean backend is running"
    }


@app.post("/analyze")
async def analyze_video(file: UploadFile = File(...)):

    print("\n========== MOHANLEAN ANALYSIS STARTED ==========")

    # 1. Save uploaded video
    print("STEP 1: Saving uploaded video...")

    os.makedirs("uploads", exist_ok=True)

    video_path = os.path.join(
        "uploads",
        file.filename
    )

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print(f"Video saved: {video_path}")

    # 2. Extract frames
    print("STEP 2: Extracting frames...")

    extract_frames(
        video_path,
        "frames",
        sample_rate=5
    )

    print("Frame extraction complete.")

    # 3. Detect pose
    print("STEP 3: Detecting body pose...")

    pose_data = analyze_frames("frames")

    print("Pose detection complete.")

    # Save pose data
    with open("pose_data.json", "w") as pose_file:
        json.dump(
            pose_data,
            pose_file,
            indent=2
        )

    print("Pose data saved.")

    # 4. Calculate lean and score
    print("STEP 4: Calculating lean and score...")

    result = analyze_score()

    print("Scoring complete.")
    print("RESULT:", result)

    print("========== MOHANLEAN ANALYSIS FINISHED ==========\n")

    return result