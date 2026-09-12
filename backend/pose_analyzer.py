import cv2
import mediapipe as mp
import os
import json


mp_pose = mp.solutions.pose


def analyze_frames(frames_folder="frames"):

    results = []

    image_files = sorted([
        f for f in os.listdir(frames_folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])

    with mp_pose.Pose(
        static_image_mode=True,
        model_complexity=1,
        min_detection_confidence=0.5
    ) as pose:

        for filename in image_files:

            image_path = os.path.join(frames_folder, filename)

            image = cv2.imread(image_path)

            if image is None:
                continue

            rgb_image = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2RGB
            )

            result = pose.process(rgb_image)

            if result.pose_landmarks:

                landmarks = []

                for landmark in result.pose_landmarks.landmark:

                    landmarks.append({
                        "x": landmark.x,
                        "y": landmark.y,
                        "z": landmark.z,
                        "visibility": landmark.visibility
                    })

                results.append({
                    "frame": filename,
                    "detected": True,
                    "landmarks": landmarks
                })

            else:

                results.append({
                    "frame": filename,
                    "detected": False,
                    "landmarks": []
                })

    return results


if __name__ == "__main__":

    data = analyze_frames()

    detected = sum(
        1 for frame in data
        if frame["detected"]
    )

    print(f"Total frames: {len(data)}")
    print(f"Frames with pose detected: {detected}")

    # Save the results
    with open("pose_data.json", "w") as file:
        json.dump(data, file, indent=2)

    print("Pose data saved to pose_data.json")  