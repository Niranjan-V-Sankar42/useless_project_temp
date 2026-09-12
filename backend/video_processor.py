import cv2
import os


def extract_frames(video_path, output_folder="frames", sample_rate=5):

    if os.path.exists(output_folder):
        for old_file in os.listdir(output_folder):
            old_path = os.path.join(output_folder, old_file)

            if os.path.isfile(old_path):
                os.remove(old_path)

    os.makedirs(output_folder, exist_ok=True)

    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print("Could not open video")
        return 0

    fps = video.get(cv2.CAP_PROP_FPS)

    frame_number = 0
    saved_frames = 0

    frame_interval = max(1, int(fps / sample_rate))

    while True:

        success, frame = video.read()

        if not success:
            break

        if frame_number % frame_interval == 0:

            filename = os.path.join(
                output_folder,
                f"frame_{saved_frames:04d}.jpg"
            )

            cv2.imwrite(filename, frame)

            saved_frames += 1

        frame_number += 1

    video.release()

    return saved_frames


if __name__ == "__main__":

    video_path = "test.mp4"

    count = extract_frames(video_path)

    print(f"Extracted {count} frames")