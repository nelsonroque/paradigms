# LIBRARIES
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# base libs
from __future__ import division
from math import cos, sin, sqrt, atan2, degrees
import time
import random

def getAngle1(A,B):
    deltaX = B[0] - A[0]
    deltaY = B[1] - A[1]
    if(deltaX > 0):
        bearing = 90 - degrees(atan2(deltaY,deltaX))
    elif(deltaX < 0):
        bearing = 270 - degrees(atan2(deltaY,deltaX))
    elif(deltaX == 0):
        if(deltaY > 0):
            bearing = 0
        elif(deltaY < 0):
            bearing = 180
        elif(deltaY == 0):
            bearing = 'NA'
    if(bearing == 0):
        bearing = 360
    return(bearing)
    
def getAngle2(A,B):
    deltaX = B[0] - A[0]
    deltaY = B[1] - A[1]
    
    return(bearing)
    
def gb(A,B):
    center_y = A[1]
    center_x = A[0]
    x = B[0]
    y = B[1]
    angle = degrees(atan2(y - center_y, x - center_x))
    bearing1 = (angle + 360) % 360
    bearing2 = (90 - angle) % 360
    print "gb: x=%2d y=%2d angle=%6.1f bearing1=%5.1f bearing2=%5.1f" % (x, y, angle, bearing1, bearing2)
    return(bearing1,bearing2)

# create test cases
ang_vec = range(-200,200,50)

print(ang_vec)

for ang in ang_vec:
    for ang2 in ang_vec:
        print("---")
        print(ang,ang2)
        print(gb([0,0],[ang,ang2]))
        print(getAngle1([0,0],[ang,ang2]))