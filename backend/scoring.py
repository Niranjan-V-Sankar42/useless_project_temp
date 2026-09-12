import json
import math
import os
import shutil


def calculate_torso_lean(landmarks):
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_HIP = 23
    RIGHT_HIP = 24

    left_shoulder = landmarks[LEFT_SHOULDER]
    right_shoulder = landmarks[RIGHT_SHOULDER]
    left_hip = landmarks[LEFT_HIP]
    right_hip = landmarks[RIGHT_HIP]

    shoulder_x = (left_shoulder["x"] + right_shoulder["x"]) / 2
    shoulder_y = (left_shoulder["y"] + right_shoulder["y"]) / 2

    hip_x = (left_hip["x"] + right_hip["x"]) / 2
    hip_y = (left_hip["y"] + right_hip["y"]) / 2

    dx = shoulder_x - hip_x
    dy = hip_y - shoulder_y

    if dy <= 0:
        return None

    angle = math.degrees(math.atan(abs(dx) / abs(dy)))

    return angle


def calculate_score(lean_angle):
    if lean_angle < 2:
        return 20
    elif lean_angle < 4:
        return 40
    elif lean_angle < 6:
        return 55
    elif lean_angle < 8:
        return 70
    elif lean_angle < 10:
        return 80
    elif lean_angle < 12:
        return 90
    elif lean_angle <= 15:
        return 100
    else:
        return 100


def analyze_score():

    with open("pose_data.json", "r") as file:
        data = json.load(file)

    angles = []

    for frame in data:

        if not frame["detected"]:
            continue

        angle = calculate_torso_lean(frame["landmarks"])

        if angle is not None and 0 <= angle <= 60:

            angles.append({
                "frame": frame["frame"],
                "angle": angle
            })

    if not angles:
        return {
            "success": False,
            "message": "No valid pose detected"
        }

    # Find maximum lean
    max_frame = max(angles, key=lambda x: x["angle"])

    max_lean_angle = max_frame["angle"]
    max_lean_frame = max_frame["frame"]

    # -----------------------------
    # SAVE MAXIMUM LEAN FRAME
    # -----------------------------

    frames_folder = "frames"
    results_folder = "results"

    os.makedirs(results_folder, exist_ok=True)

    source_frame = os.path.join(
        frames_folder,
        max_lean_frame
    )

    output_frame = os.path.join(
        results_folder,
        "max_lean_frame.jpg"
    )

    if os.path.exists(source_frame):
        shutil.copy2(
            source_frame,
            output_frame
        )

    # -----------------------------
    # REPRESENTATIVE LEAN
    # -----------------------------

    sorted_angles = sorted(
        angles,
        key=lambda x: x["angle"]
    )

    count = max(
        1,
        math.ceil(len(sorted_angles) * 0.20)
    )

    strongest_angles = sorted_angles[-count:]

    lean_angle = sum(
        item["angle"] for item in strongest_angles
    ) / len(strongest_angles)

    # -----------------------------
    # SCORE
    # -----------------------------

    score = calculate_score(lean_angle)

    return {
        "success": True,
        "lean_angle": round(lean_angle, 2),
        "max_lean_angle": round(max_lean_angle, 2),
        "max_lean_frame": "results/max_lean_frame.jpg",
        "score": score,
        "valid_frames": len(angles)
    }


if __name__ == "__main__":

    result = analyze_score()

    print()
    print("MohanLean Result")
    print("----------------")
    print(
        f"Lean Angle: "
        f"{result.get('lean_angle', 'N/A')} degrees"
    )
    print(
        f"Maximum Lean: "
        f"{result.get('max_lean_angle', 'N/A')} degrees"
    )
    print(
        f"Maximum Lean Frame: "
        f"{result.get('max_lean_frame', 'N/A')}"
    )
    print(
        f"Score: "
        f"{result.get('score', 'N/A')}/100"
    )
    print(
        f"Valid Frames: "
        f"{result.get('valid_frames', 0)}"
    )