from Realsense.realsense_depth import *
from Realsense.realsense import *
from Algorithm.main import *
import cv2


# Initialize Camera Intel Realsense
dc = DepthCamera()

# Create window for video
cv2.namedWindow("Video")

# Get CV model
model = get_model()

while True:
    ret, depth_frame, color_frame = dc.get_frame()
    if ret:
        coordinates = get_coordinates(color_frame, model)
        if coordinates != None:
            print(coordinates)
            depth = process_frame(depth_frame, int(coordinates[0]), int(coordinates[1]), int(coordinates[2]), int(coordinates[3]))
            print(depth)