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

# for circle
CIRCLE_GROW_SPEED = 0.93
CIRCLE_GROW_DIR = "+"
CIRCLE_SCALE_INIT = 1
CIRCLE_COLOR = "black"
CIRCLE_RADIUS = 1
CIRCLE_THICKNESS = 3

# for cue
CUE_COLOR = "green"
CUE_TYPE = "flash"
CUE_TIME = .3
CUE_THICKNESS = 6
CUE_SIZE_GRID = range(60,300,15)

# for mask
MASK_WIDTH = 200
MASK_HEIGHT = 200
MASK_POSITION = [0,0]

# demo params
N_TRIALS = 10
TASK_VERSION = "ZOOM"
RETENTION_TIME = 1.2

# FUNCTIONS
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# draw fixation
def draw_fixation(type,screen_time):
    fixation = visual.TextStim(win, text="+",pos=[0,0],color="black")
    fixation.draw()
    if(screen_time != -1):
        win.flip()
        core.wait(screen_time)
    
# draw cue
def draw_screen_cue(win,CUE_RADIUS,CUE_THICKNESS,CUE_TYPE,CUE_TIME):
    cue = visual.Circle(win, pos=[0,0], lineColor=CUE_COLOR, lineWidth=CUE_THICKNESS, radius=CUE_RADIUS)
    draw_fixation("cross",-1)
    cue.draw()
    win.flip()
    core.wait(CUE_TIME)

# wait for response
def draw_screen_response(win,CUE_RADIUS,CUE_THICKNESS,CUE_TYPE):
    # specify max sweep circle size
    CIRCLE_MAX = CUE_RADIUS + 20

    # initialize counter to keep track of total orientation changes before response
    update_count = 0

    # start timer for response
    start_time = time.time()

    # build objects
    cue = visual.Circle(win, pos=[0,0], lineColor=CUE_COLOR, lineWidth=CUE_THICKNESS, radius=CUE_RADIUS)
    sweeper = visual.Circle(win, pos=[0,0], lineColor=CIRCLE_COLOR, lineWidth=CIRCLE_THICKNESS, radius=CIRCLE_RADIUS)

    # initialize object scale
    sweeper.size = CIRCLE_SCALE_INIT
    CIRCLE_SCALE = CIRCLE_SCALE_INIT
    reset_count = 0
    while not event.getKeys():
        # increment circle
        
        if(CIRCLE_GROW_DIR == "+"):
            sweeper.size += CIRCLE_GROW_SPEED
            CIRCLE_SCALE += CIRCLE_GROW_SPEED
        else:
            sweeper.size -= CIRCLE_GROW_SPEED
            CIRCLE_SCALE -= CIRCLE_GROW_SPEED

        # reset circle back to initial size
        if(CIRCLE_SCALE >= CIRCLE_MAX):
            sweeper.size = 1
            CIRCLE_SCALE = 1
            sweeper.radius = CIRCLE_RADIUS
            reset_count += 1

        # draw sweeper
        draw_fixation("cross",-1)
        sweeper.draw()

        # draw cue
        if CUE_TYPE == "constant":
           cue.draw()
        
        # update line
        win.flip()
        
        # update counter
        update_count += 1

    # end trial timer
    end_time = time.time()

    # PERFORMANCE METRICS
    # =========================================

    # extract RT
    RT = end_time - start_time

    # calculate difference beteween (postive means overshoot) 
    sweeper_end_radius = sweeper.radius*sweeper.size
    radial_diff = round(sweeper_end_radius-cue.radius,1)
    
    return(RT,sweeper_end_radius,radial_diff,update_count,reset_count,sweeper.size,sweeper.radius,sweeper_end_radius)

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
header = ["timestamp","version","trial","retention_time_secs","update_count","reset_count","sweeper_growth_speed","sweeper_start_scaling_factor","sweeper_end_scaling_factor","sweeper_start_radius","sweeper_end_radius","cue_radius","radial_difference","RT"]
header_str = ",".join(header)
header_str += "\n"
df.write(header_str)

# create window
win = visual.Window(color='white',units='pix',fullscr=True)

# run experiment: trial flow (cue -> mask -> response -> feedback)
for trial in range(0,N_TRIALS):
    tst = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    # select CUE_LOCATION from annulus grid
    CUE_RADIUS = random.choice(CUE_SIZE_GRID)

    # run trial
    draw_screen_cue(win,CUE_RADIUS,CUE_THICKNESS,CUE_TYPE,CUE_TIME)
    RT,sweeper_end_radius,radial_diff,update_count,reset_count,sweeper_size,sweeper_radius,sweeper_end_radius = draw_screen_response(win,CUE_RADIUS,CUE_THICKNESS,CUE_TYPE)

    # organize trial data
    trial_data = [tst,TASK_VERSION,str(trial),str(RETENTION_TIME),str(update_count),str(reset_count),str(CIRCLE_GROW_SPEED),str(CIRCLE_SCALE_INIT),str(sweeper_size),str(sweeper_radius),str(sweeper_end_radius),str(CUE_RADIUS),str(radial_diff),str(RT)]
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