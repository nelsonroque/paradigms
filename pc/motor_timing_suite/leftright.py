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
LINE_LENGTH = 50
LINE_THICKNESS = 12
FONT_HEIGHT=64
STIM_GRID = ["left","left-arrow","right","right-arrow"]

# demo params
N_TRIALS = 60
TASK_VERSION = "LEFT_RIGHT"

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
def draw_screen_cue(win,CUE):
    
    if(CUE == "left-arrow"):
        decide_case = "NA"
        cue = visual.ImageStim(win, image="img/left.png")
    elif(CUE == "right-arrow"):
        decide_case = "NA"
        cue = visual.ImageStim(win, image="img/right.png")
    elif(CUE == "left"):
        decide_case = random.choice(["LEFT","left"])
        cue = visual.TextStim(win, text=decide_case, color="black",height=FONT_HEIGHT)
    elif(CUE == "right"):
        decide_case = random.choice(["RIGHT","right"])
        cue = visual.TextStim(win, text=decide_case, color="black",height=FONT_HEIGHT)

    # start trial timer
    start_time = time.time()
    
    # draw cue
    cue.draw()
    win.flip()
    
    # wait for kb
    k = ['']
    while k[0] not in ['escape', 'esc', 'left', 'right']:
        k = event.waitKeys()

        # end trial timer
        end_time = time.time()

    # PERFORMANCE METRICS
    # =========================================

    # extract RT
    RT = end_time - start_time
    
    # response var
    response = k[0]
    
    # calculate accuracy
    if(CUE == "left" or CUE == "left-arrow"):
        SIDE = "L"
    elif(CUE == "right" or CUE == "right-arrow"):
        SIDE = "R"
        
    if(response == "left" and SIDE == "L"):
        ACC = 1
    elif(response == "right" and SIDE == "R"):
        ACC = 1
    else:
        ACC = 0
    
    return(response, decide_case, RT, ACC)


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
header = ["timestamp","version","trial","RT","ACC","cue","case_shown","user_response"]
header_str = ",".join(header)
header_str += "\n"
df.write(header_str)

# create window
win = visual.Window(color='white',units='pix',fullscr=True)

# run experiment: trial flow (cue -> mask -> response -> feedback)
for trial in range(0,N_TRIALS):
    tst = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    # select CUE_LOCATION from annulus grid
    CUE = random.choice(STIM_GRID)

    # run trial
    draw_fixation("cross",1)
    response, decide_case, RT, ACC = draw_screen_cue(win,CUE)

    # organize trial data
    trial_data = [tst,TASK_VERSION,str(trial),str(RT),str(ACC),CUE,decide_case,response]
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