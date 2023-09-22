import time
import os
import pickle
import csv
from rotpy.system import SpinSystem
from rotpy.camera import CameraList
import asyncio

system = SpinSystem()
cameras = CameraList.create_from_system(system, update_cams=True, update_interfaces=True)

async def save_to_disk_async(batch, file_path):
    with open(file_path, "wb") as f:
        pickle.dump(batch, f)

async def save_item_async(item, file_path):
    with open(file_path, "wb") as f:
        pickle.dump(item, f)

async def save_individual_items(batch, base_file_path):
    tasks = [save_item_async(item, f"{base_file_path}_item_{i}.pkl") for i, item in enumerate(batch)]
    await asyncio.gather(*tasks)

def acquire_images_common(cam_index, date_folder, curr_trial, frame_rate, barrier, cam_folder, duration):
    print(f"Starting body camera {cam_index+1}")
    camera = cameras.create_camera_by_index(cam_index)
    camera.init_cam()

    resolution = (camera.camera_nodes.Height.get_node_value(), camera.camera_nodes.Width.get_node_value())
    print(resolution)
    
    # TODO: probably can be hardcoded
    resolution = (600, 960)
    
    camera.begin_acquisition()
    start_time = time.time()
    
    # TODO: need to remove all the samples parts
    print(f'samples_body_{cam_index+1}.csv')
    if os.path.isfile(f'samples_body_{cam_index+1}.csv'):
        os.remove(f'samples_body_{cam_index+1}.csv')
    
    batch = []
    fps_list = []

    while time.time() - start_time < duration:
        fps_start = time.time()
        image_count = int((time.time() - start_time) * frame_rate)
        image = camera.get_next_image()
        raw_data = image.get_image_data()
        batch.append(raw_data)
        image.release()
        
        fps_end = time.time()
        timestamp = int(time.perf_counter() * 1e6)
        fps = 1 / (fps_end - fps_start)
        fps_list.append([timestamp, fps])

    with open(f'samples_body_{cam_index+1}.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(fps_list)

    base_file_path = f"{date_folder}/{cam_folder}/raw/{curr_trial}/batch_{time.time()}_{cam_index+1}"
    asyncio.run(save_individual_items(batch, base_file_path))
    batch = []

    camera.end_acquisition()
    camera.deinit_cam()
    camera.release()
