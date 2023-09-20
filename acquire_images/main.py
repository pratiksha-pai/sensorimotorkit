import datetime
import multiprocessing
import cv2
import os
import pickle
from common_utils import init_structure, get_folder_count, convert_pickle_to_png
from body_cam import acquire_images_common
from dart_cam import acquire_dart_images

if __name__ == "__main__":
    date_folder = os.path.join("../", datetime.datetime.now().strftime("%Y-%m-%d"))
    init_structure(date_folder)

    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    frame_rate_1 = 120.0  # Body cameras
    acquire_time = 1.0  # Acquire for 1 seconds

    curr_trail = (get_folder_count(os.path.join(date_folder, 'dart_tracking', 'raw')) -1) if get_folder_count(os.path.join(date_folder, 'dart_tracking', 'raw')) > 0 else 0
    # ^ is this a bug pratiksha? thinkkkk, esssh write better logic here please


    barrier = multiprocessing.Barrier(3)

    process1 = multiprocessing.Process(target=acquire_images_common, args=(0, date_folder, curr_trail, frame_rate_1, barrier, 'body_tracking/camera_1', acquire_time))
    process2 = multiprocessing.Process(target=acquire_images_common, args=(1, date_folder, curr_trail, frame_rate_1, barrier, 'body_tracking/camera_2', acquire_time))
    process3 = multiprocessing.Process(target=acquire_dart_images, args=(0, date_folder, curr_trail, 30, barrier, 'dart_tracking', acquire_time))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()

    # call the load_data_from_pkl.py
    resolution_body_cam = (1200, 1920)
    resolution_dart_cam = (3, 480, 640)

    convert_pickle_to_png(os.path.join(date_folder, 'body_tracking/camera_1/raw', str(curr_trail)), resolution_body_cam)
    convert_pickle_to_png(os.path.join(date_folder, 'body_tracking/camera_2/raw', str(curr_trail)), resolution_body_cam)
    # convert_pickle_to_png(os.path.join(date_folder, 'dart_tracking/raw', str(curr_trail)), resolution_dart_cam)


    cv2.destroyAllWindows()
