from turtle import color
from matplotlib.pyplot import show
from Realsense.realsense_depth import *
from Realsense.realsense import *
from Algorithm.main import *
import cv2


# Initialize Camera Intel Realsense
dc = DepthCamera()

# Create window for video
cv2.namedWindow("Video")
cv2.namedWindow("Video_Depth")

# Get CV model
model = get_model()

while True:
    ret, depth_frame, color_frame = dc.get_frame()
    print(ret)
    if ret:

        key = cv2.waitKey(1)
        if key == 27:
            break
        coordinates = get_coordinates(color_frame, model)
        #coordinates = None
        if coordinates != None:
            print(coordinates)
            depth = process_frame(
                depth_frame, coordinates[0], coordinates[1], coordinates[2], coordinates[3])
            print(coordinates)
            #show_frame(color_frame, depth, coordinates)
            print(depth)
        cv2.imshow("Video", color_frame)
        cv2.imshow("Video_Depth", depth_frame)
