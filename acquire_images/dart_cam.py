import cv2
import time
import os
import pickle
from common_utils import get_folder_count

def acquire_dart_images(cam_index, date_folder, curr_trial, frame_rate, barrier, cam_folder, duration):
    print(f"Starting dart camera {cam_index+1}")
    cap = cv2.VideoCapture(cam_index)
    ret, frame = cap.read()
    if not ret:
        print("Failed to open Dart camera.")
        return

    frame_rate = 30  # Dart camera
    resolution = frame.shape[:2]
    print(f"Dart camera resolution: {resolution}")

    # index = (get_folder_count(os.path.join(date_folder, cam_folder, 'raw')) - 1) if get_folder_count(os.path.join(date_folder, cam_folder, 'raw')) > 0 else 0

    start_time = time.time()
    while time.time() - start_time < duration:
        # barrier.wait()
        fps_start = time.time()
        ret, frame = cap.read()
        if not ret:
            print("Failed to acquire image from Dart camera.")
            break
        
        image_count = int((time.time() - start_time) * frame_rate)
        

        try:
            with open(f"{date_folder}/{cam_folder}/raw/{curr_trial}/frame_{image_count}_{cam_index+1}.pkl", "wb") as f:
                pickle.dump(frame, f)
            # cv2.imwrite(f"{date_folder}/{cam_folder}/raw/{curr_trial}/frame_{image_count}_{cam_index+1}.png", frame)
        except Exception:
            break

        fps_end = time.time()
        fps = 1 / (fps_end - fps_start)
        # print(f"Dart {cam_index+1} FPS: {fps}")
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
