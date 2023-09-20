from rotpy.camera import CameraList
import cv2
import numpy as np
import time
import os
import pickle
from rotpy.system import SpinSystem
from rotpy.camera import CameraList

system = SpinSystem()
cameras = CameraList.create_from_system(system, update_cams=True, update_interfaces=True)

def acquire_images_common(cam_index, date_folder, curr_trial, frame_rate, barrier, cam_folder, duration):
    print(f"Starting body camera {cam_index+1}")
    camera = cameras.create_camera_by_index(cam_index)
    camera.init_cam()

    resolution = (camera.camera_nodes.Height.get_node_value(), camera.camera_nodes.Width.get_node_value()) 
    # TODO ^ probably can be hardcoded
    print(resolution)
    resolution = (1200, 1920)
    
    
    camera.begin_acquisition()

    start_time = time.time()

    # TODO need to remove all the samples parts
    if os.path.isfile(f'samples_body_{cam_index+1}.txt'):
        os.remove(f'samples_body_{cam_index+1}.txt')
    
    while time.time() - start_time < duration:
        # barrier.wait()
        fps_start = time.time()
        image_count = int((time.time() - start_time) * frame_rate)
        image = camera.get_next_image()
        raw_data = image.get_image_data()

        try:
            with open(f"{date_folder}/{cam_folder}/raw/{curr_trial}/frame_{image_count}_{cam_index+1}.pkl", "wb") as f:
                pickle.dump(raw_data, f)
        except Exception:
            break # TODO need better handling here

        image.release()

        fps_end = time.time()
        fps = 1 / (fps_end - fps_start)
        with open(f'samples_body_{cam_index+1}.txt', 'a') as f: # TODO check if this is adding to the delay?
            f.write(f"{fps}\n")

        if cv2.waitKey(1) & 0xFF == 27:
            break

    camera.end_acquisition()
    camera.deinit_cam()
    camera.release()


