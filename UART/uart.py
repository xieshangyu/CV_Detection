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
