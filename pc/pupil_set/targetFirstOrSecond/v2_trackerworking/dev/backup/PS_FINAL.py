'''
PUPIL SIZE + ATTENTION SET EXPERIMENT
CODE BY: NELSON ROQUE

TO-DO:
    CHECK THE DATA
    REPLCAEMENT WITH NO LAST TRIAL SAME
'''

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# IMPORTS --------------------------------------->
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import os
import re
import time
import random
import datetime
import pylink as pl
import pylinkwrapper
from psychopy import visual, event, core, gui

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# CLASSES --------------------------------------->
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

class ConfigData:
    def __init__(self,var2search):
        self.file = "config.txt" # name of your configuration file in the project dir

        self.var2search = var2search
        self.type = ''
        self.value = ''

    def getValue(self):
        if self.value == '':
            df = open(self.file,"r")
            itemList = df.readlines()
            for item in itemList :
                raw = item
                raw = raw.rstrip()
                split1 = raw.split(":") # name:value|type
                name = split1[0]
                value = split1[1].split("|")[0]
                type = split1[1].split("|")[1]

                if(self.var2search == name):
                    self.type = type

                    if(self.type == "int"):
                        self.value = int(value)
                    elif(self.type == "float"):
                        self.value = float(value)
                    elif(self.type == "str"):
                        self.value = str(value)
                    elif(self.type == "strlist"):
                        val_list = value.split(",")
                        self.value = []
                        for val in val_list:
                            self.value.append(str(val))
                    elif(self.type == "strlist2"):
                        val_list = value.split("***")
                        self.value = []
                        for val in val_list:
                            self.value.append(str(val))
            return(self.value)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# EYETRACKING FUNCTIONS ------------------------->
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def LOG_MSG(el,lstr):
    el.send_message('EXP_LOG|' + lstr)

def trackerInit(part_file):
    el = pylinkwrapper.Connect(win, part_file)
    return(el)
    
def askCalibration():
    calibrate = visual.TextStim(win,text="EXPERIMENTER:\nDO NOT ADVANCE THIS SCREEN\n\nUNTIL CAMERA SETUP IS COMPLETE,\n\nPress spacebar to Continue, then click CALIBRATE on the Eyetracking PC")
    calibrate.draw()
    win.flip()
    k = ['']
    count = 0
    start_time = time.time()
    while k[0] not in ['escape','esc','space','spacebar']:
        if(k[0] == 'escape' or k[0] == 'esc'):
            quit
        k = event.waitKeys()

def calibrationDisplay(el,cnum,paval,win):
    # Calibrate eye-tracker
    el.calibrate(cnum,paval)
    return(1)

def openEDF(dfn,el):
    og = dfn
    dfn = os.path.splitext(dfn)[0]  # strip away extension if present
    assert re.match(r'\w+$', dfn), 'Name must only include A-Z, 0-9, or _'
    assert len(dfn) <= 8, 'Name must be <= 8 characters.'
    el.openDataFile(og)
    pl.flushGetkeyQueue()
    #el.setOfflineMode()

def endExperiment(el,save_path):
    # show message for saving data
    savingData = visual.TextStim(win,text="Transferring EDF files...please wait")
    savingData.draw()
    win.flip()

    # receive the data file
    el.end_experiment(save_path)


#def saveBitmap():
    # 10 arguments (get from documentation)
    #pl.bitmapSave()

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# EXPERIMENT FUNCTIONS -------------------------->
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def showColors():
    # setup all boxes and labels
    greyBox = visual.Rect(win, width=90,height=90,fillColor="darkgrey", pos=[-100,0])
    whiteBox = visual.Rect(win, width=90,height=90,fillColor="white", pos=[0,0])
    blackBox = visual.Rect(win, width=90,height=90,fillColor="black", pos=[100,0])
    greyLabel = visual.TextStim(win, text="GRAY",color="darkgrey", pos=[-100,-100])
    whiteLabel = visual.TextStim(win, text="WHITE",color="white", pos=[0,-100])
    blackLabel = visual.TextStim(win, text="BLACK",color="black", pos=[100,-100])

    # instruction for boxes
    instruct = visual.TextStim(win, text="The letter you will be searching for will always be black or white, and the rest of the letters will be gray",pos=[0,200])
    
    # draw all boxes
    instruct.draw()
    
    # draw all labels
    greyLabel.draw()
    whiteLabel.draw()
    blackLabel.draw()
    greyBox.draw()
    whiteBox.draw()
    blackBox.draw()
    win.flip()
    
    # wait for response
    k = ['']
    count = 0
    start_time = time.time()
    while k[0] not in ['escape','esc','space','spacebar']:
        if(k[0] == 'escape' or k[0] == 'esc'):
            quit
        k = event.waitKeys()

def playInstructions(inst_list):
    for inst in inst_list:
        # prepare instruct
        cur_inst = visual.TextStim(win,text=inst,height=36,pos=[0,200])
        space_continue = visual.TextStim(win,text="Press SPACEBAR to continue",pos=[0,-200])

        # draw instructions
        cur_inst.draw()
        space_continue.draw()
        win.flip()

        # wait for participant input to advance
        k = ['']
        count = 0
        start_time = time.time()
        while k[0] not in ['escape','esc','space','spacebar']:
            if(k[0] == 'escape' or k[0] == 'esc'):
                core.quit()
            k = event.waitKeys()

def getTargetPositions(stream_length,lag_points_list):
    targ_positions = []
    for lag in lag_points_list:
        lag_index = int(stream_length*lag)
        targ_positions.append(lag_index)
    return(targ_positions)

def genStreamItems(numItems):
    # no I, O, W, Z because Leber & Egeth, 2006
    possible_stim = ['A','B','C','D','E','F','G','H','J','K','L','M','N','P','Q','R','S','T','U','V','X','Y']

    # initialize counter/list
    stim_count = 0
    item_list = []

    # generate rand Stim
    while(stim_count < numItems):
        chosenOne = random.choice(possible_stim)
        item_list.append(chosenOne)
        stim_count = stim_count + 1
    return(item_list)

def genStreamItems2(numItems):
    # no I, O, W, Z because Leber & Egeth, 2006
    possible_stim = ['A','B','C','D','E','F','G','H','J','K','L','M','N','P','Q','R','S','T','U','V','X','Y']

    # initialize counter/list
    stim_count = 0
    item_list = []

    # generate rand Stim
    while(stim_count < numItems):
        chosenOne = random.choice(possible_stim)
        nextChosenOne = random.choice(possible_stim)
        while(chosenOne == nextChosenOne):
            nextChosenOne = random.choice(possible_stim)
        item_list.append(chosenOne)
        item_list.append(nextChosenOne)
        stim_count = stim_count + 2
    return(item_list)

def playVisualCue(TARG_COLOR):
    INSTRUCT_SIZE = 60
    INSTRUCT_SUB_SIZE = INSTRUCT_SIZE/2

    # create instructions for search
    targ_i = visual.TextStim(win,text="Your target letter is:".upper(),height=INSTRUCT_SUB_SIZE,color="darkgrey",pos=[0,100])
    search = visual.TextStim(win,text=TARG_COLOR,height=INSTRUCT_SIZE,color='darkgrey')
    cont = visual.TextStim(win,text="Press spacebar to continue".upper(),height=INSTRUCT_SUB_SIZE,color='darkgrey',pos=[0,-100])

    # draw instructions to the screen
    targ_i.draw()
    search.draw()
    cont.draw()
    win.flip()

    # create log mesage to send
    log_str = "|cue_ON|"

    # if tracker connected, send log msgs
    if(TRACKER_CONNECTED):
        LOG_MSG(el,log_str)

    # wait for a space response
    k = ['']
    count = 0
    start_time = time.time()
    while k[0] not in ['escape','esc','space','spacebar']:
        if(k[0] == 'escape' or k[0] == 'esc'):
            quit
        k = event.waitKeys()
    end_time = time.time()

    # create log mesage to send
    log_str = "|cue_OFF|"

    # if tracker connected, send log msgs
    if(TRACKER_CONNECTED):
        LOG_MSG(el,log_str)

    # get RT to response
    return(end_time-start_time)

def playRSVPStream(item_list,targ_index,target_color,speed_s,MYTRIAL):
    # simple error checking for target out of bounds
    if(targ_index > (len(item_list) - 1)):
        print("ERROR: TARGET INDEX OUT OF RANGE")

    # set distractor colors, based on Leber & Egeth, 2006
    exp_colors = ['darkgrey']#['purple','red','green','blue']

    # logic for setting distractor color
    if(target_color == "black"):
        dist_color = "white"
        dist2_color = "darkgrey"
    else:
        dist_color = "black"
        dist2_color = "darkgrey"

    # init stim counter
    stim_index = 0

    # init lists for collection
    color_str = []
    letter_str = []

    # wait 200 ms before beginning stream
    core.wait(.2)

    # create log mesage to send
    log_str = "|stream_ON|"

    # if tracker connected, send log msgs
    if(TRACKER_CONNECTED):
        LOG_MSG(el,log_str)

    # run stream
    while(stim_index < len(item_list)):
        if(stim_index == targ_index): # frame at target
            stim_color = target_color
            letter_stim = item_list[stim_index]
            target_letter = letter_stim
            stim = visual.TextStim(win,letter_stim,color=stim_color,height=LETTER_SIZE)
            
            # generate log message
            log_str = "target_ON"

            # if tracker connected, send log msgs
            if(TRACKER_CONNECTED):
                LOG_MSG(el,log_str)
        elif(stim_index == (targ_index + 1)): # frame after target
            stim_color = dist_color
            letter_stim = item_list[stim_index]
            dist_post_letter = letter_stim
            stim = visual.TextStim(win,letter_stim,color=stim_color,height=LETTER_SIZE)
        elif(stim_index == (targ_index - 1)): # frame before target
            #stim_color = dist2_color # uncomment for more difficult judgement
            rand_color = random.choice(exp_colors)
            stim_color = rand_color
            letter_stim = item_list[stim_index]
            dist_pre_letter = letter_stim
            stim = visual.TextStim(win,letter_stim,color=stim_color,height=LETTER_SIZE)
        else: # all other frames
           rand_color = random.choice(exp_colors)
           stim_color = rand_color
           letter_stim = item_list[stim_index]
           stim = visual.TextStim(win,letter_stim,color=stim_color,height=LETTER_SIZE)

        # draw the stim to screen
        stim.draw()
        win.flip()

        # wait for letter presentation time
        core.wait(speed_s)

        # generate log message
        log_str = "trial:" + str(MYTRIAL) + "|" + "color:" + stim_color + "|" + "letter:" + letter_stim

        # if tracker connected, send log msgs
        if(TRACKER_CONNECTED):
            LOG_MSG(el,log_str)

        # save color and letter data for all
        color_str.append(stim_color)
        letter_str.append(letter_stim)

        # increment stimuli counter
        stim_index = stim_index + 1

    # join all letters/colors with a comma
    letter_str = ":".join(letter_str)
    color_str = ":".join(color_str)
    
    # create log mesage to send
    log_str = "|stream_OFF|"

    # if tracker connected, send log msgs
    if(TRACKER_CONNECTED):
        LOG_MSG(el,log_str)


    return(target_letter, dist_pre_letter, dist_post_letter, letter_str, color_str)

def responseScreen(target_color):
    INSTRUCT_SIZE = 60
    INSTRUCT_SUB_SIZE = INSTRUCT_SIZE/2

    # start recording
    #startRecording(File_samples, File_events, Link_samples, Link_events)
    if(TRACKER_CONNECTED):
        core.wait(.05)
        el.record_on(sendlink=True)#startRecording(1,1,1,1)
    
    # create log mesage to send
    log_str = "|response_START|"

    # if tracker connected, send log msgs
    if(TRACKER_CONNECTED):
        LOG_MSG(el,log_str)
    
    # show question to participant
    question1 = visual.TextStim(win,text="Report the letter that was:",height=INSTRUCT_SUB_SIZE,color='darkgrey',pos=[0,100])
    question2 = visual.TextStim(win,text=target_color,height=INSTRUCT_SIZE,color='darkgrey')
    question1.draw()
    question2.draw()
    win.flip()
    RESPONSE = ['']
    count = 0
    start_time = time.time()
    while RESPONSE[0] not in ['escape','esc','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
        if(RESPONSE[0] == 'escape' or RESPONSE[0] == 'esc'):
            quit
        RESPONSE = event.waitKeys()
        end_time = time.time()
        RT = end_time - start_time
    
    # create log mesage to send
    log_str = "|response_END|"

    # if tracker connected, send log msgs
    if(TRACKER_CONNECTED):
        LOG_MSG(el,log_str)
    
    # stop recording
    if(TRACKER_CONNECTED):
        core.wait(.05)
        el.record_off()#stopRecording()
    return(RT, RESPONSE[0].upper())

def single_trial(PARTICIPANT, TODAY, TRACKER_CONNECTED, TRIAL_STRING, trial_count, total_stream_length, stream_speed):
    # extract trial variables
    TRIAL_DATA = TRIAL_STRING.split("_")
    TARG_INDEX = int(TRIAL_DATA[0])
    TARG_COLOR = TRIAL_DATA[1]

    # set trial counter
    TRIAL = trial_count

    # create participant filename
    PART_FILE = 'data/data_' + str(PARTICIPANT) +'.csv'

    # open the data file
    df = open(PART_FILE,'a')

    # create log mesage to send
    log_str = "|trial_START|"

    # if tracker connected, send log msgs
    if(TRACKER_CONNECTED):
        LOG_MSG(el,log_str)

    # give cue (white / black, auditory/visual)
    CONTINUE_TIME = playVisualCue(TARG_COLOR)

    # generate items for stream
    mystream = genStreamItems2(total_stream_length)

    # start recording
    #startRecording(File_samples, File_events, Link_samples, Link_events)
    if(TRACKER_CONNECTED):
        core.wait(.05)
        el.record_on(sendlink=True)

    # play RSVP stream to participant
    TRIAL_START = time.time()
    TARG_IDEN, DIST_PRE_IDEN, DIST_POST_IDEN, LETTER_STR, COLOR_STR = playRSVPStream(mystream,TARG_INDEX,TARG_COLOR,stream_speed,TRIAL)

    # stop recording
    if(TRACKER_CONNECTED):
        core.wait(.05)
        el.record_off()

    # give response screen to participant
    RT, RESPONSE = responseScreen(TARG_COLOR)

    # create log mesage to send
    log_str = "|trial_END|"

    # if tracker connected, send log msgs
    if(TRACKER_CONNECTED):
        LOG_MSG(el,log_str)

    # determine ACC
    if(RESPONSE == TARG_IDEN):
        ACC = 1
    else:
        ACC = 0

    if(ACC == 1):
        DOES_RESP_EQUAL_TARG = 1
        DOES_RESP_EQUAL_DIST_PRE = 0
        DOES_RESP_EQUAL_DIST_POST = 0
    else:
        DOES_RESP_EQUAL_TARG = 0
        if(RESPONSE == DIST_PRE_IDEN):
            DOES_RESP_EQUAL_DIST_PRE = 1
        else:
            DOES_RESP_EQUAL_DIST_PRE = 0

        if(RESPONSE == DIST_POST_IDEN):
            DOES_RESP_EQUAL_DIST_POST = 1
        else:
            DOES_RESP_EQUAL_DIST_POST = 0

    # data to export
    EXPORT_STRING = [str(PARTICIPANT), TODAY,
                     str(TRIAL_START),str(TRIAL), str(stream_speed),
                     str(TARG_INDEX), TARG_COLOR,
                     DIST_PRE_IDEN, TARG_IDEN, DIST_POST_IDEN, RESPONSE,
                     str(ACC), str(DOES_RESP_EQUAL_DIST_PRE), str(DOES_RESP_EQUAL_TARG), str(DOES_RESP_EQUAL_DIST_POST),
                     str(RT), str(CONTINUE_TIME),
                     LETTER_STR, COLOR_STR]
    EXPORT_STRING_ = ",".join(EXPORT_STRING)
    EXPORT_STRING_ = EXPORT_STRING_ + "\n"
    df.write(EXPORT_STRING_)

    # close the data file
    df.close()
    return(PART_FILE)

def generateConditionTable(factor1_list,factor2_list):
    trial_list = []
    for item in factor1_list:
        for j in factor2_list:
            trial_list.append((str(item)+"_"+j))
    return(trial_list)
    
def getSubjectInfo(subject_number):
    if(subject_number % 2 == 0):
        subject_parity = "even"
    else:
        subject_parity = "odd"

    # define each block (list of strings will be used as trial table later)
    if(subject_parity == "odd"):
        counterbalance = [8,12]
    elif(subject_parity == "even"):
        counterbalance = [12,8]
    return(subject_parity)

def my_gui():
    myDlg = gui.Dlg(title="PS Study")
    myDlg.addText('PARTICIPANT INFORMATION')
    myDlg.addField('PARTICIPANT NUMBER:')
    myDlg.show() # show gui
    if gui.OK:
        userInfo = str(myDlg.data)
        # support for 4 Digit Participant Number
        pNum = re.findall("\d+",userInfo)
    else:
        core.quit()
    return int(pNum[0])

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# PARAMS ---------------------------------------->
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# set debugging code
DEBUG = ConfigData("DEBUG").getValue()

# set size of letters
LETTER_SIZE = ConfigData("LETTER_SIZE").getValue()

# get list of distractors
target_stream_length = ConfigData("NUM_POS_OF_INTEREST").getValue()
total_stream_length = ConfigData("STREAM_LENGTH").getValue()
stream_speed = ConfigData("STREAM_SPEED_S").getValue()

# SPECIFY targ possible colors
TARG_COLORS = ConfigData("TARG_COLORS").getValue()

# how many blocks of 10 trials (LAG x5 x COLOR)
MINI_BLOCK_MULTIPLIER = ConfigData("BLOCK_MULTIPLIER").getValue()
MINI_BLOCK_MULTIPLIER_PRAC = ConfigData("BLOCK_MULTIPLIER_PRAC").getValue()

# number of calibration targets
cnum = ConfigData("NUM_CALIBRATION_TARGETS").getValue()

# pacing of calibration (how long to fixate each targ in ms)
paval = ConfigData("CALIBRATION_FIX_TARGET_TIME_MS").getValue()

# set to 1 if tracker connected
TRACKER_CONNECTED = ConfigData("TRACKER_CONNECTED").getValue()

# target positions
LAG_1 = ConfigData("LAG_1").getValue()
LAG_2 = ConfigData("LAG_2").getValue()
LAG_3 = ConfigData("LAG_3").getValue()
LAG_POINTS = [LAG_1,LAG_2,LAG_3]
TARG_POSITIONS = getTargetPositions(total_stream_length,LAG_POINTS)

# determine size of a mini block
MINI_BLOCK_SIZE = len(TARG_COLORS) * len(LAG_POINTS)

# get list of instructions
INSTRUCTION_LIST = ConfigData("INSTRUCTIONS").getValue()

# get list of instructions
INSTRUCTION_LIST_PRAC = ConfigData("INSTRUCTIONS_PRAC").getValue()

# calculate total trials
TOTAL_TRIALS = MINI_BLOCK_SIZE * MINI_BLOCK_MULTIPLIER

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# RUN EXPERIMENT -------------------------------->
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# get participant info
if(DEBUG):
    PARTICIPANT = 999
else:
    PARTICIPANT = my_gui()
subject_parity = getSubjectInfo(PARTICIPANT)

print(PARTICIPANT)

# set today's date
TODAY_DATE = datetime.date.today()
TODAY = format(TODAY_DATE,"%m/%d/%Y")

# create participant filename
PART_FILE_ = 'data/data_' + str(PARTICIPANT)
EDF_FILE_ = str(PARTICIPANT) + '.edf'
PART_FILE = PART_FILE_ +'.csv'

# ROUTINE IF TRACKER CONNECTED
if(TRACKER_CONNECTED):
    # open window for initial instructions
    win = visual.Window(color="gray", units="pix", pos=[0,0],fullscr=True)
    
    # hide the mouse
    event.Mouse(visible=False)
    
    # instruct experimenter on calibration
    askCalibration()
    
    # open window for calibration instructions
    win = visual.Window(units='deg', fullscr=True,
                        allowGUI=False, color=0)

    # initialize the tracker
    el = trackerInit(EDF_FILE_)

    # calibrate if not debugging
    if(DEBUG):
       CAL_SUCCESS = 1
    else:
        CAL_SUCCESS = calibrationDisplay(el,cnum,paval,win)

# start the experiment if calibration exited gracefully
if(CAL_SUCCESS):
    # open window for experiment
    win = visual.Window(color="gray", units="pix", pos=[0,0],fullscr=True)

    # hide the mouse
    event.Mouse(visible=False)

    # extract window details
    sres = win.size
    sp = (sres[0], sres[1])
    scenter = [sres[0] / 2.0, sres[1] / 2.0]
    color_depth = 32

    # open the data file
    df = open(PART_FILE,'a')

    # write file header
    df.write("PARTICIPANT,DATE,TRIAL_START_SYS_TIME,TRIAL,STREAM_SPEED_S,TARG_INDEX,TARG_COLOR,DIST_PRE_TARG_IDEN,TARG_IDEN,DIST_POST_TARG_IDEN,RESPONSE_IDEN,ACC,DOES_RESP_EQUAL_DIST_PRE_TARG,DOES_RESP_EQUAL_TARG,DOES_RESP_EQUAL_DIST_POST_TARG,RT,SPACE_TO_CONTINUE_TIME,LETTER_STR,COLOR_STR\n")
    df.close()

    # define all trials
    prac_trials = generateConditionTable(TARG_POSITIONS,TARG_COLORS) * MINI_BLOCK_MULTIPLIER_PRAC
    trials = generateConditionTable(TARG_POSITIONS,TARG_COLORS) * MINI_BLOCK_MULTIPLIER

    # shuffle trials
    random.shuffle(prac_trials)
    random.shuffle(trials)
    
    # instructions
    playInstructions(INSTRUCTION_LIST_PRAC)
    
    # show all colors to participant
    showColors()

    # for quick testing, subset 6 rand trials
    if(DEBUG):
        # run blocks
        trial_count_prac = 1
        for trial in prac_trials:
            single_trial(PARTICIPANT,TODAY,TRACKER_CONNECTED,trial,trial_count_prac,total_stream_length,stream_speed)
            trial_count_prac = trial_count_prac + 1
    else:
        # run practice trials
        trial_count_prac = 1
        for trial in prac_trials:
            single_trial(PARTICIPANT,TODAY,TRACKER_CONNECTED,trial,trial_count_prac,total_stream_length,stream_speed)
            trial_count_prac = trial_count_prac + 1
            
        # instructions
        playInstructions(INSTRUCTION_LIST)

        # show all colors to participant
        showColors()
        
        # run experiment trials
        trial_count = 1
        for trial in trials:
            single_trial(PARTICIPANT,TODAY,TRACKER_CONNECTED,trial,trial_count,total_stream_length,stream_speed)
            trial_count = trial_count + 1

    # closing message
    e_experiment = visual.TextStim(win,text="Thank you for your participation!")
    e_experiment.draw()
    win.flip()
    core.wait(2)

    # end experiment and transfer EDF_FILE
    if(TRACKER_CONNECTED):
        endExperiment(el,"data/edf/")