import os
import cv2

def extract_frames(video_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        filename = os.path.join(output_folder, f"image{frame_count:03d}.jpg")
        cv2.imwrite(filename, frame)
    cap.release()
