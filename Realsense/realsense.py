import cv2
import pyrealsense2
from realsense_depth import *
import statistics

point = (400, 300)

def show_distance(event, x, y, args, params):
    global point
    point = (x, y)

# Initialize Camera Intel Realsense
dc = DepthCamera()

# Create mouse event
cv2.namedWindow("Color frame")
cv2.setMouseCallback("Color frame", show_distance)

while True:
    ret, depth_frame, color_frame = dc.get_frame()

    # Show distance for a specific point
    cv2.circle(color_frame, point, 4, (0, 0, 255))
    distance = depth_frame[point[1], point[0]]

    # Calculate bounds of 100 x 100 square around the point
    bounds = 50
    minY = point[1]-bounds
    maxY = point[1]+bounds
    minX = point[0]-bounds
    maxX = point[0]+bounds
    
    values = []
    for x in range(minX, maxX+1):
        for y in range(minY, minY+1):
            values.append(depth_frame[y, x])
            #print(depth_frame[point[1], point[0]])
    print(values)
    med = statistics.median(values)
    
    cv2.putText(color_frame, "{}mm".format(distance) + "Median: {}mm".format(med), (point[0], point[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0))
    cv2.rectangle(color_frame, (minX, minY), (maxX, maxY), (0, 0, 255), 10)

    cv2.imshow("depth frame", depth_frame)
    cv2.imshow("Color frame", color_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break