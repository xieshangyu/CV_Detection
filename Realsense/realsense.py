import cv2
import pyrealsense2
from Realsense.realsense_depth import *
import statistics

# Processes frame and returns median depth
def process_frame(depth_frame, x_min, y_min, x_max, y_max):     
    values = []
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            values.append(depth_frame[y, x])

    med = statistics.median(values)
    return med