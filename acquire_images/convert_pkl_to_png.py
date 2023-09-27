

import os
import pickle
from common_utils import convert_pickle_to_png, process_pkl_and_apply_pose
import datetime

date_folder = os.path.join("../", datetime.datetime.now().strftime("%Y-%m-%d"))

resolution_body_cam = (2, 600, 960)
resolution_dart_cam = (3, 480, 640)
process_pkl_and_apply_pose(os.path.join(date_folder, 'body_tracking/camera_1/raw', str(0)), (600, 960))
process_pkl_and_apply_pose(os.path.join(date_folder, 'body_tracking/camera_2/raw', str(0)), (600, 960))