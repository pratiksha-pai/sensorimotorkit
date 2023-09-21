from concurrent.futures import ThreadPoolExecutor
import asyncio
from rotpy.camera import CameraList
import cv2
import numpy as np
import time
import os
import pickle
import csv
from queue import Queue
from rotpy.system import SpinSystem
from rotpy.camera import CameraList

system = SpinSystem()
cameras = CameraList.create_from_system(system, update_cams=True, update_interfaces=True)

# # Initialize ThreadPoolExecutor
# executor = ThreadPoolExecutor()

async def save_to_disk_async(batch, file_path):
    # Your existing save_to_disk_async function, modified to save batches
    with open(file_path, "wb") as f:
        pickle.dump(batch, f)

async def save_batch_async(batch, file_path):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, save_to_disk_async, batch, file_path)

async def save_item_async(item, file_path):
    with open(file_path, "wb") as f:
        pickle.dump(item, f)


async def save_individual_items(batch, base_file_path):
    tasks = []
    for i, item in enumerate(batch):
        task = save_item_async(item, f"{base_file_path}_item_{i}.pkl")
        tasks.append(task)
    await asyncio.gather(*tasks)

# async def save_to_disk_async(data, file_path):
#     loop = asyncio.get_running_loop()
#     await loop.run_in_executor(executor, pickle.dump, data, open(file_path, 'wb'))

# async def save_csv_async(timestamp, fps, file_path):
#     loop = asyncio.get_running_loop()
#     await loop.run_in_executor(executor, csv.writer(open(file_path, 'a', newline='')).writerow, [timestamp, fps])

def acquire_images_common(cam_index, date_folder, curr_trial, frame_rate, barrier, cam_folder, duration):
    print(f"Starting body camera {cam_index+1}")
    camera = cameras.create_camera_by_index(cam_index)
    camera.init_cam()

    resolution = (camera.camera_nodes.Height.get_node_value(), camera.camera_nodes.Width.get_node_value()) 
    # TODO ^ probably can be hardcoded
    print(resolution)
    resolution = (1200, 1920)
    resolution = (600, 960)
    
    camera.begin_acquisition()
    start_time = time.time()
    
    # TODO need to remove all the samples parts
    print(f'samples_body_{cam_index+1}.csv')
    if os.path.isfile(f'samples_body_{cam_index+1}.csv'):
        os.remove(f'samples_body_{cam_index+1}.csv')
    
    batch = []
    fps_list = []

    while time.time() - start_time < duration:
        # barrier.wait()
        fps_start = time.time()
        image_count = int((time.time() - start_time) * frame_rate)
        image = camera.get_next_image()
        raw_data = image.get_image_data()
        batch.append(raw_data)

        # try:
        #     # await save_to_disk_async(raw_data, f"{date_folder}/{cam_folder}/raw/{curr_trial}/frame_{image_count}_{cam_index+1}.pkl")
        #     with open(f"{date_folder}/{cam_folder}/raw/{curr_trial}/frame_{image_count}_{cam_index+1}.pkl", "wb") as f:
        #         pickle.dump(raw_data, f)
        # except Exception:
        #     break # TODO need better handling here

        image.release()
        
        fps_end = time.time()
        timestamp = int(time.perf_counter() * 1e6)
        fps = 1 / (fps_end - fps_start)
        fps_list.append([timestamp, fps])

        # await save_csv_async(timestamp, fps, f'samples_body_{cam_index+1}.csv')

        # with open(f'samples_body_{cam_index+1}.csv', 'a', newline='') as f: # TODO check if this is adding to the delay?
        #     writer = csv.writer(f)
        #     writer.writerow([timestamp, fps])
        
        # if cv2.waitKey(1) & 0xFF == 27:
        #     break
    

    with open(f'samples_body_{cam_index+1}.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(fps_list)

    base_file_path = f"{date_folder}/{cam_folder}/raw/{curr_trial}/batch_{time.time()}_{cam_index+1}"
    asyncio.run(save_individual_items(batch, base_file_path))
    batch = []
    camera.end_acquisition()
    camera.deinit_cam()
    camera.release()