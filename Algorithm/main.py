import torch
import cv2

# Model
# model = torch.hub.load('ultralytics/yolov5', 'custom', path='./Algorithm/pt_files/best.pt')  # or yolov5m, yolov5l, yolov5x, custom
def get_model():
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='./Algorithm/pt_files/best.pt')  # or yolov5m, yolov5l, yolov5x, custom
    return model

def coordinate(frame, model):
    results = model(frame)                  #using the same model each frame
    multi_rows = results.pandas().xyxy[0]  
    row_1=multi_rows.head(1)                #this is the only way to return the first row of pandas coordinate
    if len(multi_rows.head(1)) != 0:
        x_min, y_min, x_max,y_max = row_1['x_min'][0], row_1['y_min'][0],row_1['x_max'][0],row_1['y_max'][0]  
        return x_min, y_min, x_max,y_max
    return None



# while(True):
#     ret, frame = vid.read()
#     if ret:
#         results = model(frame)
#         print(results.pandas().xyxy[0])