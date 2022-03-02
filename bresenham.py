import time
from time import sleep
import threading
import re
import math
import socket

DIRX, DIRY, DIRZ = 10,  9,  0 # 19, 21, 27 
STPX, STPY, STPZ =  6, 13, 21 # 31, 33, 40
ENTB             =  5         # 29
RLMP             =  1         # 28
GLMP             =  7  

CW      = 1
CCW     = 0
delay   = 0.0001
sdelay  = 0.000125
RG      = CCW
LF      = CW
FW      = CW
BW      = CCW
UP      = CW
DW      = CCW

x1, y1, z1 = 98, 129, 100
x2, y2, z2 = 150, 200, 189

def Bresenham3D(x1, y1, z1, x2, y2, z2): 
    ListOfPoints = [] 
    ListOfPoints.append((x1, y1, z1)) 
    dx = abs(x2 - x1) 
    dy = abs(y2 - y1) 
    dz = abs(z2 - z1) 
    if (x2 > x1): 
        xs = 1
    else: 
        xs = -1
    if (y2 > y1): 
        ys = 1
    else: 
        ys = -1
    if (z2 > z1): 
        zs = 1
    else: 
        zs = -1

    # Driving axis is X-axis" 
    if (dx >= dy and dx >= dz):      
        p1 = 2 * dy - dx 
        p2 = 2 * dz - dx 
        while (x1 != x2): 
            x1 += xs 
            if (p1 >= 0): 
                y1 += ys 
                p1 -= 2 * dx 
            if (p2 >= 0): 
                z1 += zs 
                p2 -= 2 * dx 
            p1 += 2 * dy 
            p2 += 2 * dz
            ListOfPoints.append((x1, y1, z1))

    # Driving axis is Y-axis" 
    elif (dy >= dx and dy >= dz):    
        p1 = 2 * dx - dy 
        p2 = 2 * dz - dy 
        while (y1 != y2): 
            y1 += ys 
            if (p1 >= 0): 
                x1 += xs 
                p1 -= 2 * dy 
            if (p2 >= 0): 
                z1 += zs 
                p2 -= 2 * dy 
            p1 += 2 * dx 
            p2 += 2 * dz 
            ListOfPoints.append((x1, y1, z1)) 

    # Driving axis is Z-axis" 
    else:        
        p1 = 2 * dy - dz 
        p2 = 2 * dx - dz 
        while (z1 != z2): 
            z1 += zs 
            if (p1 >= 0): 
                y1 += ys 
                p1 -= 2 * dz 
            if (p2 >= 0): 
                x1 += xs 
                p2 -= 2 * dz 
            p1 += 2 * dy 
            p2 += 2 * dx 
            ListOfPoints.append((x1, y1, z1))
    print(ListOfPoints)
    return ListOfPoints

def processing(dtgc):
     for i in range(len(dtgc)):
        print(i)
        if dtgc[i][0] == "G1":
            (x1, y1, z1) = xpw,  ypw,  zpw
            (x2, y2, z2) = int((dtgc[i][4]*100)),    int((dtgc[i][5]*100)),   int((dtgc[i][6]*100))
            print(x2, y2, z2)
        ListOfPoints = Bresenham3D(x1, y1, z1, x2, y2, z2)
        multpros(ListOfPoints)

def multpros(ListOfPoints):
    for e in range(len(ListOfPoints)-1):
        if ListOfPoints[e][0]<ListOfPoints[e+1][0]:
            DIR1X=RG
        elif ListOfPoints[e][0]>ListOfPoints[e+1][0]:
            DIR1X=LF
        else:
            DIR1X=2
        if ListOfPoints[e][1]<ListOfPoints[e+1][1]:
            DIR1Y=FW
        elif ListOfPoints[e][1]>ListOfPoints[e+1][1]:
            DIR1Y=BW
        else :
            DIR1Y=2
        if ListOfPoints[e][2]<ListOfPoints[e+1][2]:
            DIR1Z=UP
        elif ListOfPoints[e][2]>ListOfPoints[e+1][2]:
            DIR1Z=DW
        else :
            DIR1Z=2
        XMOV = threading.Thread(target=mot, args=(STPX, DIRX, DIR1X))
        YMOV = threading.Thread(target=mot, args=(STPY, DIRY, DIR1Y))
        ZMOV = threading.Thread(target=mot, args=(STPZ, DIRZ, DIR1Z))
        XMOV.start()
        YMOV.start()
        ZMOV.start()
        XMOV.join()
        YMOV.join()
        ZMOV.join()
def mot(STEPn, DIRn, DIR):
    global CW, CCW, STPX, STPY, STPZ
    tot_step = 4 ## gerakan 0.01
    if DIR != 2:
        GPIO.output(DIRn, DIR)
        for y in range(tot_step):
            GPIO.output(STEPn, GPIO.HIGH)
            sleep(sdelay)
            GPIO.output(STEPn, GPIO.LOW)
            sleep(sdelay)
processing()
