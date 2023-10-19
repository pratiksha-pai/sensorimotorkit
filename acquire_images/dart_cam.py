import cv2
import time
import os
import pickle
import asyncio


async def save_to_disk_async(batch, file_path):
    with open(file_path, "wb") as f:
        pickle.dump(batch, f)

async def save_item_async(item, file_path):
    with open(file_path, "wb") as f:
        pickle.dump(item, f)

async def save_individual_items(batch, base_file_path):
    print("=====================FILE PATH=====================")
    print(base_file_path)
    tasks = [save_item_async(item, f"{base_file_path}_item_{i}.pkl") for i, item in enumerate(batch)]
    await asyncio.gather(*tasks)

def acquire_dart_images(cam_index, date_folder, curr_trial, frame_rate, barrier, cam_folder, duration):
    print(f"Starting dart camera {cam_index+1}")
    cap = cv2.VideoCapture(cam_index)
    ret, frame = cap.read()
    if not ret:
        print("Failed to open Dart camera.")
        return
    
    # check if base file path exists
    # f"{date_folder}/{cam_folder}/raw/{curr_trial}/batch_{time.time()}_{cam_index+1}"
    if not os.path.exists(f"{date_folder}/{cam_folder}/raw/{curr_trial}"):
        print(f"Creating folder for dart camera {date_folder}/{cam_folder}/raw/{curr_trial}/batch_{time.time()}_{cam_index+1}")
        os.makedirs(f"{date_folder}/{cam_folder}/raw/{curr_trial}")

    frame_rate = 30  # Dart camera
    resolution = frame.shape[:2]

    start_time = time.time()

    # TODO need to remove all the samples parts
    if os.path.isfile(f'samples_dart_{cam_index+1}.txt'):
        os.remove(f'samples_dart_{cam_index+1}.txt')
    batch = []
    while time.time() - start_time < duration:
        # barrier.wait()
        fps_start = time.time()
        ret, frame = cap.read()
        if not ret:
            print("Failed to acquire image from Dart camera.")
            break
        
        image_count = int((time.time() - start_time) * frame_rate)

        batch.append(frame)

        # try:
        #     with open(f"{date_folder}/{cam_folder}/raw/{curr_trial}/frame_{image_count}_{cam_index+1}.pkl", "wb") as f:
        #         pickle.dump(frame, f)
        # except Exception:
        #     break

        fps_end = time.time()
        # fps = 1 / (fps_end - fps_start)
        # with open(f'samples_dart_{cam_index+1}.txt', 'a') as f:
        #     f.write(f"{fps}\n")

        if cv2.waitKey(1) & 0xFF == 27:
            break

    base_file_path = f"{date_folder}/{cam_folder}/raw/{curr_trial}/batch_{time.time()}_{cam_index+1}"
    asyncio.run(save_individual_items(batch, base_file_path))
    batch = []

    cap.release()
