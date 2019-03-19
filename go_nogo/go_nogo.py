"""
Go-NoGo Task
Code by Nelson Roque (roque@psy.fsu.edu)
"""

# =======================================================================================
# LIBRARIES
# =======================================================================================

from __future__ import division
from psychopy import visual, event, core, gui
import random
import time
from time import gmtime, strftime
#import serial # for sending EEG triggers

# =======================================================================================
# FUNCTIONS
# =======================================================================================

def drawInstruction(instruction):
    INSTRUCT = visual.TextStim(win, instruction)
    INSTRUCT.draw()
    win.flip()
    k = ['']
    while k[0] not in ['escape','esc','space','spacebar']:
        k = event.waitKeys()

# =======================================================================================
# TIMING PARAMETERS
# =======================================================================================

FIXATION_OPTIONS = [400,450,500,550,600]
STIMULUS_PRESENTATION_TIME = 200/1000 # conversion to milliseconds
STIMULUS_MASK_TIME = 50/1000
FEEDBACK_TIME = 400/1000
BLINK_TIME = 2000/1000

# =======================================================================================
# EXPERIMENT PARAMETERS
# =======================================================================================

DEBUG_CODE = 1

if(DEBUG_CODE):
    N_GO_TRIALS = 6
    N_NOGO_TRIALS = 2
else:
    N_GO_TRIALS = 350
    N_NOGO_TRIALS = 150

# create trial list (type of trial * repetitions)
TRIAL_LIST = ['G'] * N_GO_TRIALS
TRIAL_LIST += ['NG'] * N_NOGO_TRIALS

# shuffle that list so presentation is random
random.shuffle(TRIAL_LIST)

# =======================================================================================
# STIMULI PARAMETERS
# =======================================================================================

GO_TRIAL_STRING = 'SSSTSSS'
NOGO_TRIAL_STRING = 'SSSHSSS'
MASK_STRING = 'XXXXXXX'

# =======================================================================================
# EEG PARAMETERS
# =======================================================================================

# SERIAL_PORT = serial.Serial(0, 57600, timeout=1)  # open first serial port & give it a name 

# =======================================================================================
# GET SESSION PARAMETERS
# =======================================================================================

# GET PARTICIPANT INFO
dlg = gui.Dlg(title="Go No-Go Task", pos=(200, 400))
dlg.addField('Participant #', 999)

# OPEN GUI TO GET INFO
SESSION = dlg.show()  # you have to call show() for a Dlg (automatic with a DlgFromDict)    
if dlg.OK:
    # get session info
    SESSION_TIMESTAMP = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    PARTICIPANT = SESSION[0]
else:
    print('User cancelled')
    core.quit()

# open the data file for writing
PARTICIPANT_FILENAME = 'data/'+'data_' + str(PARTICIPANT) + ".txt"
df = open(PARTICIPANT_FILENAME,'a')

# write data header
TRIAL_DATA = ["PARTICIPANT", "SESSION_TIMESTAMP", "TRIAL_N", "CURRENT_TRIAL", "TRIAL_TYPE", "TRIAL_START_TIME", "FIXATION_ONSET_TIME", "STIM_ONSET_TIME", "MASK_ONSET_TIME", "RESPONSE_GIVEN_TIME", "RT_REL_STIM_ONSET", "RT_REL_MASK_ONSET", "ACCURACY", "TIMEOUT"]
TRIAL_DATA = "\t".join(TRIAL_DATA)
TRIAL_DATA += "\n"
df.write(TRIAL_DATA)

# =======================================================================================
# GIVE INSTRUCTIONS
# =======================================================================================

# open a window
win = visual.Window(fullscr=True)

# give instructions
drawInstruction("In this task, you will be asked to respond when you see the following item on screen\n\nSSSTSSS\n\nPress spacebar to continue")
drawInstruction("Do not responsd when you see this item:\n\nSSSHSSS\n\nPress spacebar to continue")
drawInstruction("When you see the word BLINK on screen, please blink during this 2 second window\n\nPress spacebar to continue")
drawInstruction("Press spacebar to begin the experiment")

# =======================================================================================
# RUN THE EXPERIMENT
# =======================================================================================

# for each trial
TRIAL_N = 1
for trial in TRIAL_LIST:
    TRIAL_START_TIME = time.time()
    
    # send trigger to EEG
    #SERIAL_PORT.write('TRIAL_ON')
    
    if(TRIAL_N % 5 == 0):
         # display fixation cross
        TRIAL_TYPE = "BLINK"
        BLINK_MSG = visual.TextStim(win,"BLINK")
        BLINK_MSG.draw()
        win.flip()
        core.wait(BLINK_TIME)
    else:
        TRIAL_TYPE = "NON_BLINK"

    # get trial info
    CURRENT_TRIAL = trial

    # get fix time
    FIXATION_TIME = random.choice(FIXATION_OPTIONS)/1000 # conversion to milliseconds

    # display fixation cross
    FIXATION_CROSS = visual.TextStim(win,"+")
    FIXATION_CROSS.draw()
    win.flip()
    FIXATION_ONSET_TIME = time.time()
    core.wait(FIXATION_TIME)

    # based on trial type create appropriate stimuli
    if(CURRENT_TRIAL == 'G'):
        EXP_STIM = visual.TextStim(win,GO_TRIAL_STRING)
    elif(CURRENT_TRIAL == 'NG'):
        EXP_STIM = visual.TextStim(win,NOGO_TRIAL_STRING)

    # draw stimuli
    EXP_STIM.draw()
    win.flip()
    STIM_ONSET_TIME = time.time()
    
    # send trigger to EEG
    #SERIAL_PORT.write('STIM_ON')
    core.wait(STIMULUS_PRESENTATION_TIME)

    # draw mask
    MASK_STIM = visual.TextStim(win,MASK_STRING)
    MASK_STIM.draw()
    win.flip()
    MASK_ONSET_TIME = time.time()
    
    # send trigger to EEG
    #SERIAL_PORT.write('MASK_ON')
    core.wait(STIMULUS_MASK_TIME)

    # listen for a response
    k = ['']
    while k[0] not in ['escape', 'esc','space','spacebar']:
        k = event.waitKeys(maxWait=1,keyList=['space','spacebar','escape','esc'])
        if k == None:
            END_TIME = time.time()
            TIMEOUT = 1
            
            # send trigger to EEG
            #SERIAL_PORT.write('TIMEOUT')
            break
        else:
            END_TIME = time.time()
            TIMEOUT = 0
            
            # send trigger to EEG
            #SERIAL_PORT.write('RESPONSE')
            break
    
    # calculate RT relative to stimulus onset
    RT=END_TIME-STIM_ONSET_TIME
    
    # calculate RT relative to mask onset
    RT2=END_TIME-MASK_ONSET_TIME
    
    if(TIMEOUT):
        # calculate accuracy
        if(CURRENT_TRIAL == 'G'):
            ACCURACY = 0
        elif(CURRENT_TRIAL == 'NG'):
            ACCURACY = 1
    else:
        # calculate accuracy
        if(CURRENT_TRIAL == 'G'):
            ACCURACY = 1
        elif(CURRENT_TRIAL == 'NG'):
            ACCURACY = 0

    # display feedback for inaccurate trials
    if(ACCURACY == 0):
        FEEDBACK = visual.TextStim(win, "ERROR")
        FEEDBACK.draw()
        win.flip()
        core.wait(FEEDBACK_TIME)
    
    # save the data
    TRIAL_DATA = [PARTICIPANT, SESSION_TIMESTAMP, TRIAL_N, CURRENT_TRIAL, TRIAL_TYPE, TRIAL_START_TIME, FIXATION_ONSET_TIME, STIM_ONSET_TIME, MASK_ONSET_TIME, END_TIME, RT, RT2, ACCURACY, TIMEOUT]
    
    # convert all elements to strings
    TRIAL_DATA_STR = []
    for item in TRIAL_DATA:
        item = str(item)
        TRIAL_DATA_STR.append(item)
    
    # concatenate all elements tab-delimited and add a newline at the end
    TRIAL_SAVE_STRING = "\t".join(TRIAL_DATA_STR)
    TRIAL_SAVE_STRING += "\n"
    df.write(TRIAL_SAVE_STRING)
    
    # send trigger to EEG
    #SERIAL_PORT.write('TRIAL_OFF')
    
    # increment trial counter
    TRIAL_N += 1

# =======================================================================================
# EXPERIMENT EXIT
# =======================================================================================
df.close()
drawInstruction("Thank you for your participation today!\n\nPress spacebar to save and exit")