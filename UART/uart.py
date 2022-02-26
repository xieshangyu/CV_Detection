# Ammaar
import time
import serial

count = 0

ser = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)


def send_cords(horiz_disp, vert_disp):
    global count
    global ser
    data = (str(horiz_disp) + ","+str(vert_disp))
    ser.write(data.encode())
    count += 1

    
def determine_move(obj_x_coord,obj_y_coord,xres,yres):
    centerx,centery = xres/2,yres/2
    
    move_x = obj_x_coord-centerx
    move_y = obj_y_coord-centery 
    if(move_x != 0):
        move_x /= abs(obj_x_coord-centerx)
    if(move_y != 0):
        move_y /= abs(obj_y_coord-centery)
  
    return(movex,movey)
