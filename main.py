import os
from turtle import color
from matplotlib.pyplot import show
from Realsense.realsense_depth import *
from Realsense.realsense import *
from Algorithm.main import *
import cv2
import time
import argparse
# Disable tensorflow output
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def main(_argv):
    parser = argparse.ArgumentParser()
    # Initialize Camera Intel Realsense
    dc = DepthCamera()

    Debug_flag = 0

    # Parse arguments
    if _argv.Debug == "1" or _argv.D == "1":
        Debug_flag = 1
        # Create window for video
        cv2.namedWindow("Video")
        cv2.namedWindow("Video_Depth")

    elif _argv.Debug == "0" or _argv.D == "0":
        Debug_flag = 0

    # Load saved CV model
    model = get_model()

    # Initialize Algorithm
    oldCords = None
    depth = None

    while True:
        # Start Video Capture
        ret, depth_frame, color_frame = dc.get_frame()

        # If frame is not empty
        if ret:

            key = cv2.waitKey(1)
            if key == 27:
                break

            # Get coordinates from color frame
            coordinates = get_coordinates(color_frame, model)

            if coordinates != None:
                # Get Median Depth from depth frame
                depth = process_frame(
                    depth_frame, coordinates[0], coordinates[1], coordinates[2], coordinates[3])

                # Debug mode
                if Debug_flag == 1:
                    print(coordinates)
                    print(coordinates)
                    print(depth)
                    show_frame(color_frame, depth_frame, depth, coordinates)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])