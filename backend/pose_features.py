import json
import math


def calculate_torso_lean(landmarks):

    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12

    LEFT_HIP = 23
    RIGHT_HIP = 24

    left_shoulder = landmarks[LEFT_SHOULDER]
    right_shoulder = landmarks[RIGHT_SHOULDER]

    left_hip = landmarks[LEFT_HIP]
    right_hip = landmarks[RIGHT_HIP]

    # Find the center of the shoulders
    shoulder_x = (
        left_shoulder["x"] + right_shoulder["x"]
    ) / 2

    shoulder_y = (
        left_shoulder["y"] + right_shoulder["y"]
    ) / 2

    # Find the center of the hips
    hip_x = (
        left_hip["x"] + right_hip["x"]
    ) / 2

    hip_y = (
        left_hip["y"] + right_hip["y"]
    ) / 2

    # Calculate how much the shoulders
    # are leaning relative to the hips

    dx = shoulder_x - hip_x
    dy = hip_y - shoulder_y

    if dy == 0:
        return 90

    angle = math.degrees(
        math.atan(abs(dx) / abs(dy))
    )

    return angle


# Load pose data
with open("pose_data.json", "r") as file:
    data = json.load(file)


angles = []

for frame in data:

    if not frame["detected"]:
        continue

    angle = calculate_torso_lean(
        frame["landmarks"]
    )

    # Ignore impossible/noisy detections
    if 0 <= angle <= 60:
        angles.append(angle)


if not angles:

    print("No valid lean data found.")

else:

    average_angle = sum(angles) / len(angles)
    maximum_angle = max(angles)

    print(f"Valid frames: {len(angles)}")
    print(f"Average torso lean: {average_angle:.2f} degrees")
    print(f"Maximum torso lean: {maximum_angle:.2f} degrees")