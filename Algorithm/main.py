import torch
import cv2

# Model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='./pt_files/best.pt')  # or yolov5m, yolov5l, yolov5x, custom

# define a video capture object
vid = cv2.VideoCapture(0)

while(True):
    ret, frame = vid.read()
    if ret:
        results = model(frame)
        print(results.pandas().xyxy[0])