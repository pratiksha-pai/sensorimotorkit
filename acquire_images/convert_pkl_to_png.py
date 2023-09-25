'''
currently this function is not integrated into main, which should be the case

'''

import os
import pickle
from common_utils import convert_pickle_to_png
import datetime

date_folder = os.path.join("../", datetime.datetime.now().strftime("%Y-%m-%d"))

resolution_body_cam = (2, 600, 960)
resolution_dart_cam = (3, 480, 640)
convert_pickle_to_png(os.path.join(date_folder, 'body_tracking/camera_1/raw', str(1)), (600, 960))
convert_pickle_to_png(os.path.join(date_folder, 'body_tracking/camera_2/raw', str(1)), (600, 960))