import os
import pickle
import cv2
import numpy as np
import os

resolution = (1200, 1920)
rotation = cv2.ROTATE_90_COUNTERCLOCKWISE


def get_folder_count(folder):
    return len([name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))])

def get_file_count(folder):
    return len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))])

def init_structure(date_folder):
    cams_structure = {
        'body_tracking/camera_1': ['raw'],
        'body_tracking/camera_2': ['raw'],
        'dart_tracking': ['raw']
    }
    for cam, folders in cams_structure.items():
        for folder in folders:
            raw_path = os.path.join(date_folder, cam, folder)
            os.makedirs(raw_path, exist_ok=True)
            index = get_folder_count(raw_path)
            os.makedirs(os.path.join(raw_path, str(index)), exist_ok=True)

def convert_pickle_to_png(folder_path, resolution=(480, 640), rotation=cv2.ROTATE_90_COUNTERCLOCKWISE):
    """
    Convert pickle files in the folder to PNG images.
    
    Parameters:
        folder_path (str): Path to the folder containing pickle files.
        resolution (tuple): Resolution to reshape the image to. Default is (480, 640).
        rotation (int): Rotation flag from cv2. Default is cv2.ROTATE_90_COUNTERCLOCKWISE.
        
    Returns:
        None
    """

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pkl'):
            with open(os.path.join(folder_path, file_name), 'rb') as f:
                raw_data = pickle.load(f)
            
            frame = np.array(raw_data).reshape(resolution)
            frame = cv2.rotate(frame, rotation)
            
            png_file_name = file_name.replace('.pkl', '.png')
            cv2.imwrite(os.path.join(folder_path, png_file_name), frame)
            # print(f"Converted {file_name} to {png_file_name}")

