# LIBRARIES
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# base libs
from __future__ import division
from math import cos, sin, sqrt, atan2, degrees
import time
import datetime
import random

# psychopy libs
from psychopy import visual, event, core
from psychopy.visual import ShapeStim

# SCREEN PARAMS
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# for cue
CUE_COLOR = 'red'
CUE_SIZE = 10
CUE_TYPE = "flash"
CUE_ANNULUS_GRID = [[200,0],[0,200],[-200,0],[0,-200],[200,200],[200,-200],[-200,200],[-200,-200]]

# for mask
MASK_WIDTH = 200
MASK_HEIGHT = 200
MASK_POSITION = [0,0]

# for line
LINE_COLOR = 'black'
LINE_LENGTH = 200
LINE_THICKNESS = 6
LINE_START_ANGLE = 30
LINE_MOVE_SPEED = 5.2
LINE_SWEEP_DIRECTION = "+"

# demo params
N_TRIALS = 6
TASK_VERSION = "SWEEP"
RETENTION_TIME = 1.2

# CLASSES
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# construct Cue class
class Cue:
    def __init__(self,x_pos,y_pos,color,size):
        origin = [0,0]
        self.position = [x_pos,y_pos]
        self.color = color
        self.size = size
        self.stim = visual.Circle(win,radius=self.size,pos=self.position,lineColor=self.color,fillColor=self.color)
        self.angle1, self.angle2 = getAngle(origin,self.position)

# construct Mask class
class Pixel:
    def __init__(self,x_pos,y_pos,color):
        self.position = [x_pos,y_pos]
        self.color = color
        self.stim = visual.Circle(win,radius=1,pos=self.position,lineColor=self.color,fillColor=self.color)

# FUNCTIONS
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def wrapTo360(angle):
    new_angle = angle % 360
    
    if(new_angle == 0):
        new_angle = 360
    return(new_angle)

def getDistance(p0, p1):
    distance = sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
    return(distance)

def getAngle(A,B):
    center_y = A[1]
    center_x = A[0]
    x = B[0]
    y = B[1]
    angle = degrees(atan2(y - center_y, x - center_x))
    bearing1 = (angle + 360) % 360
    bearing2 = (90 - angle) % 360
    #print "gb: x=%2d y=%2d angle=%6.1f bearing1=%5.1f bearing2=%5.1f" % (x, y, angle, bearing1, bearing2)
    return(bearing1,bearing2)

def draw_screen_cue(win,loc,screen_time):
    cue = Cue(loc[0],loc[1],CUE_COLOR,CUE_SIZE)
    cue.stim.draw()
    win.flip()
    core.wait(screen_time)
    return(cue.angle1,cue.angle2)
    
# draw fixation
def draw_fixation(type,screen_time):
    fixation = visual.TextStim(win, text="+",pos=[0,0],color="black")
    fixation.draw()
    win.flip()
    core.wait(screen_time)
    
def draw_screen_mask(win,screen_time):
    # generate mask grid
    for x in range(MASK_WIDTH):
        for y in range(MASK_HEIGHT):
            pixel_color = random.choice(["white","black"])
            print(x,y)
            #pixel = Pixel(x,y,pixel_color)
            #pixel.stim.draw()
    win.flip()
    core.wait(screen_time)

def draw_screen_response(win,cue_loc,cue_type):
    #sweeper = visual.Rect(win,width=LINE_THICKNESS,height=LINE_LENGTH,lineColor=LINE_COLOR,fillColor=LINE_COLOR,pos=[0,0],ori=0)
    sweeper = visual.Line(win, start=(0 - LINE_LENGTH/2, 0 - LINE_LENGTH/2), end=(0 + LINE_LENGTH/2, 0 + LINE_LENGTH/2), lineWidth=LINE_THICKNESS, lineColor=LINE_COLOR,fillColor=LINE_COLOR,pos=[0,0],ori=0)
    
    # initialize counter to keep track of total orientation changes before response
    update_count = 0

    # based on cue type, show cue throughout response (easy condition)
    if cue_type == "constant":
        # create cue object
        cue = Cue(cue_loc[0],cue_loc[1],CUE_COLOR,CUE_SIZE)
    
    # start timer for response
    start_time = time.time()
    while not event.getKeys():
        # update sweeper (orientation)
        sweeper.setOri(LINE_MOVE_SPEED, LINE_SWEEP_DIRECTION)

        # draw sweeper
        sweeper.draw()
        
        # draw cue
        if cue_type == "constant":
           cue.stim.draw()

        # update line
        win.flip()
        
        # update counter
        update_count += 1
        
        # get number of rotations (0-N)
        sweeper_rotations = sweeper.ori/360
        
        # normalize orientation
        
        # compare orientation from cue and orientation from line
        if(sweeper.ori < 360):
            sweeper_orientation_abs = sweeper.ori
        else:
            sweeper_orientation_abs = wrapTo360(sweeper.ori)

    # end trial timer
    end_time = time.time()
    
    # extract RT
    RT = end_time - start_time
    
    # print(sweeper.ori,sweeper_orientation_abs,sweeper_rotations,update_count)
    
    # return last orientation for giving feedback
    sweeper_last_ori = sweeper.ori
    sweeper_last_ori_wrap = sweeper_orientation_abs
    
    return(RT,sweeper.start,sweeper.end,sweeper_last_ori,sweeper_last_ori_wrap,sweeper_rotations,update_count)

def draw_screen_feedback(win,cue_loc,cue_angle1,cue_angle2,line_angle,RT,n_rotations, n_updates,screen_time,verbal_feedback):
    # create sweeper at last position
    sweeper = visual.Line(win, start=(0 - LINE_LENGTH/2, 0 - LINE_LENGTH/2), end=(0 + LINE_LENGTH/2, 0 + LINE_LENGTH/2), lineWidth=LINE_THICKNESS, lineColor=LINE_COLOR,fillColor=LINE_COLOR,pos=[0,0],ori=line_angle)

    # create cue object
    cue = Cue(cue_loc[0],cue_loc[1],"blue",CUE_SIZE+20)
    
    # transform line angle to be in range of 0-360
    t_line_angle = wrapTo360(line_angle)
    
    if(verbal_feedback):
        # create text feedback
        feedback_text1 = visual.TextStim(win,text="Your response took: " + str(round(RT,2)) + " seconds",color="black",pos=[0,-300])
        feedback_text2 = visual.TextStim(win,text="Cue angle 1: " + str(cue_angle1) + "-- cue angle 2: "+ str(cue_angle2) + " | line angle: " + str(t_line_angle),color="black",pos=[0,-400])
        feedback_text3 = visual.TextStim(win,text="total rotations: " + str(round(n_rotations,1)) + " | total orientation updates: " + str(round(n_updates,0)),color="black",pos=[0,-500])
        
    # draw to screen
    cue.stim.draw()
    sweeper.draw()
    if(verbal_feedback):
        feedback_text1.draw()
        feedback_text2.draw()
        feedback_text3.draw()
    win.flip()
    core.wait(screen_time)

# START TASK
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# read config file

# get GUI input
participant = 1

# construct filename
#ts = time.strftime("%Y%m%d-%H%M%S")
filename = 'data/data_' + TASK_VERSION + "_" + str(participant) + "_"+time.strftime("%Y%m%d-%H%M%S")+'.csv'

# create data file
df = open(filename,'a')

# write header
header = ["timestamp","version","trial","retention_time_secs","cue_type","line_sweep_direction","cue_pos_x","cue_pos_y","top_line_x","top_line_y","bottom_line_x","bottom_line_y","RT","n_rotations","n_updates","cue_angle1", "cue_angle2", "line_angle", "line_angle_wrap360"]
header_str = ",".join(header)
header_str += "\n"
df.write(header_str)

# create window
win = visual.Window(color='white',units='pix',fullscr=True)

# run experiment: trial flow (cue -> mask -> response -> feedback)
for trial in range(0,N_TRIALS):
    tst = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    # select CUE_LOCATION from annulus grid
    CUE_LOCATION = random.choice(CUE_ANNULUS_GRID)

    # run trial
    CUE_ANGLE1, CUE_ANGLE2 = draw_screen_cue(win,CUE_LOCATION,.5)
    draw_fixation(type,RETENTION_TIME)
    RT, SWEEP_START, SWEEP_END, LAST_ORIENTATION, LAST_ORI_WRAP, N_ROTATIONS, N_UPDATES = draw_screen_response(win,CUE_LOCATION,CUE_TYPE)
    draw_screen_feedback(win,CUE_LOCATION,CUE_ANGLE1,CUE_ANGLE2,LAST_ORIENTATION,RT,N_ROTATIONS, N_UPDATES,1,0)
    
    # organize trial data
    trial_data = [tst,TASK_VERSION,str(trial),str(RETENTION_TIME),str(CUE_TYPE),str(LINE_SWEEP_DIRECTION),str(CUE_LOCATION[0]),str(CUE_LOCATION[1]),str(SWEEP_START[0]),str(SWEEP_START[1]),str(SWEEP_END[0]),str(SWEEP_END[1]),str(RT),str(N_ROTATIONS), str(N_UPDATES), str(CUE_ANGLE1), str(CUE_ANGLE2),str(LAST_ORIENTATION),str(LAST_ORI_WRAP)]
    trial_str = ",".join(trial_data)
    trial_str += "\n"
    
    # write trial data
    df.write(trial_str)

# close the data file
df.close()

# closing message
thankyou = visual.TextStim(win,color="black",text="Task is now complete.\n\nThank you for your participation.")
thankyou.draw()
win.flip()
core.wait(2)