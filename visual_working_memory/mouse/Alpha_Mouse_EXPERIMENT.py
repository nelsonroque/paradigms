# ==================================================================
# VSTM Task
# modeled after [citation]
# code by Nelson Roque | roque@psy.fsu.edu
# ==================================================================

# Imports
# ==================================================================
from psychopy import visual, event, core, logging, gui
from math import cos, sin, radians, sqrt
from random import shuffle, randint, choice
from time import time, clock
import datetime
import re

# Classes
# ==================================================================
class ChangeSquare: # Create class for pill stimuli
    def __init__(self,position,posLabel,color,identity,isChange,squareSize):
        self.squareSize = squareSize
        self.position = position
        self.positionLabel = posLabel
        self.color = color
        self.identity = identity
        self.isChangeTrial = isChange
        self.stim = visual.Rect(win, width=self.squareSize, height=self.squareSize, fillColor=self.color, lineColor=self.color,units='pix', pos=self.position)

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

class Data: # Create class for block structure
    def __init__(self,block,trial,trial_type,setSize,RT,Click_X,Click_Y,targ_x,targ_y,TARG_START_COLOR,TARG_END_COLOR,isObjTarget,isTimeoutTrial):
        DISTANCE_THRESHOLD = SQUARE_SIZE/2

        self.block = block
        self.trial = trial
        self.trial_type = trial_type
        self.setSize = setSize
        self.RT = RT
        self.click_x = Click_X
        self.click_y = Click_Y
        self.targ_x = targ_x
        self.targ_y = targ_y
        self.isClickedTarget = isObjTarget
        self.timeout = isTimeoutTrial

        if(self.click_x == "NA"):
            self.distance = "NA"
            self.responded = False
        else:
            self.distance = sqrt(((self.click_x - self.targ_x)**2) + ((self.click_y - self.targ_y)**2))
            self.responded = True

        # calculate accuracy
        if(self.responded):
            if(self.trial_type == "change"):
                if(self.isClickedTarget == "change"):
                    self.accuracy = 1
                else:
                    self.accuracy = 0
            elif(self.trial_type == "noChange"):
                if(self.isClickedTarget == "noChange"):
                    self.accuracy = 1
                else:
                    self.accuracy = 0
        else:
            self.accuracy = 0

        if self.timeout:
            self.RT = "NA"

        self.start_color = TARG_START_COLOR
        self.end_color = TARG_END_COLOR

    def genWriteString(self):
        write_list = [str(unicode(datetime.datetime.now())),str(self.block),str(self.trial),str(self.trial_type),str(self.setSize),str(self.RT),str(self.accuracy),str(self.timeout),self.isClickedTarget,str(self.targ_x),str(self.targ_y),str(self.click_x),str(self.click_y),self.start_color,self.end_color]
        write_str = "\t".join(write_list)
        write_str = write_str + "\n"
        return(write_str)

class Instructions:
    def __init__(self,headline_text,headline_height,current_instruct,instructs_list,instruct_height,font_color):
        # other components
        self.font_color = font_color

        # headline of instructions
        self.headline_text = headline_text
        self.headline_height = headline_height
        self.headline = visual.TextStim(win,text=self.headline_text, height=self.headline_height, color=self.font_color, pos=[0,600])

        # main body of instructions
        self.current_instruct = current_instruct
        self.instruct_height = instruct_height
        self.INSTRUCTS_LIST = instructs_list
        self.instruct = visual.TextStim(win,text=self.current_instruct, height=self.instruct_height, wrapWidth=1200, color=self.font_color)

        # continue key
        self.continue_key = visual.Rect(win,width=800,height=300,pos=[0,-500], lineColor=self.font_color)
        self.continue_height = 40
        self.continue_text = visual.TextStim(win,text="CLICK ANY MOUSE BUTTON TO CONTINUE", height=self.continue_height, color=self.font_color, pos=[0,-500])

        # response keys

    def drawAll(self):
        for current_instruction in self.INSTRUCTS_LIST:
            self.current_instruct = current_instruction
            self.instruct = visual.TextStim(win,text=self.current_instruct, height=self.instruct_height, wrapWidth=1200, color=self.font_color)

            mymouse = event.Mouse()

            clickResponse = False
            while(not clickResponse):
                mouse1, mouse2, mouse3 = mymouse.getPressed()
                if(mouse1 or mouse2 or mouse3):
                    clickResponse = True

                # draw objects
                self.headline.draw()
                self.instruct.draw()
                self.continue_key.draw()
                self.continue_text.draw()
                win.flip()

# Utility Functions
# ==================================================================
def genBlock(blockSize,setSize,trials_types,returnRandom):
    #df = open("block_struct.txt","w")
    p = 0
    trial_strings = list()
    for i in range(blockSize):
        for j in trials_types:
            #df.write(str(p) + "\t" + str(j) + "\t" + str(setSize) + "\n")
            trial_string = str(j) + "_" + str(setSize)
            trial_strings.append(trial_string)
            p +=1
    if(returnRandom):
        shuffle(trial_strings)
    return(trial_strings)

def colors2sample(n,colors):
    colors=list(colors)
    if(n/len(colors) == 1) and (n%len(colors) == 0):
        n_lists = 1
    elif(n/len(colors) == 1) and (n%len(colors) > 0):
        n_lists = 2
    elif(n/len(colors) == 2) and (n%len(colors) == 0):
        n_lists = 2
    elif(n/len(colors) == 2) and (n%len(colors) > 0):
        n_lists = 3

    color_lists = list()
    for i in range(n_lists):
        color_lists.append(colors)

    i=0
    trial_colors = list()
    while(i<n):
        #print i
        if(i == 0):
            col = list(color_lists[0])
        elif(i % len(colors) == 0):
            col = list(color_lists[1])
        shuffle(col)
        sample = col.pop()
        trial_colors.append(sample)
        i+=1
    return(trial_colors)

def getGridLocations(screen_height,screen_width,buffer,window_buffer,isWidescreen):
    #transform buffer for later math
    buffer = -buffer
    window_buffer = -window_buffer

    # get usable screen real-estate for symmetrical grid
    usable_x = screen_width + window_buffer
    usable_y = usable_x

    # get rectangular bounds
    x_lower_bound = 0 - (usable_x/2)
    x_upper_bound = 0 + (usable_x/2)
    y_lower_bound = 0 - (usable_y/2)
    y_upper_bound = 0 + (usable_y/2)

    # grid dimensions
    grid_x = 6
    grid_y = 6
    grid = [grid_x,grid_y]

    if(grid[0] == grid[1]):
        #print("grid is square")
        grid_type="square"
    else:
        print("ERROR: grid is not square | contact roque@psy.fsu.edu for more information")
        grid_type="other"

    grid_cell_size = usable_x/grid[0]
    grid_cell_center = (grid_cell_size/2) - buffer

    c1 = x_lower_bound + (1*(grid_cell_center))
    c2 = x_lower_bound + (2*(grid_cell_center))
    c3 = x_lower_bound + (3*(grid_cell_center))
    c4 = x_upper_bound - (3*(grid_cell_center))
    c5 = x_upper_bound - (2*(grid_cell_center))
    c6 = x_upper_bound - (1*(grid_cell_center))
    row_x = (c1,c2,c3,c4,c5,c6)

    r1 = y_lower_bound + (1*(grid_cell_center))
    r2 = y_lower_bound + (2*(grid_cell_center))
    r3 = y_lower_bound + (3*(grid_cell_center))
    r4 = y_upper_bound - (3*(grid_cell_center))
    r5 = y_upper_bound - (2*(grid_cell_center))
    r6 = y_upper_bound - (1*(grid_cell_center))
    col_y = (r1,r2,r3,r4,r5,r6)

    col_indices = [0,1,2,3,4,5]
    grid_locations = list()
    for i in row_x:
        for j in col_indices:
            loc = [i,col_y[j]]
            grid_locations.append(loc)

    return(grid_locations)

def writeData(filename,writeParam,STRING):
    df = open(filename,writeParam)
    df.write("\t".join(STRING)+"\n")
    df.close()

def writeDataString(filename,writeParam,STRING):
    df = open(filename,writeParam)
    df.write(STRING)
    df.close()

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

# Visual Functions
# ==================================================================
def my_gui():
    myDlg = gui.Dlg(title="VSTM")
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

def drawFixation(dot_size):
    fix_dot_size = dot_size
    fixdot_inner = visual.Circle(win, radius=(fix_dot_size/2), fillColor = "black", pos=[0,0])
    fixdot_outer = visual.Circle(win, radius=fix_dot_size, fillColor = "white", pos=[0,0])
    fixdot_outer.draw()
    fixdot_inner.draw()

def drawObjList(objs):
    for i in objs:
        i.draw()

def drawResponseButtons(button_size,screen_width,screen_height):
    DEBUG_CODE = 0

    if(DEBUG_CODE):
        response_label_color = "white"
        response_box_outline = "black"
        response_box_fill = "black"
    else:
        response_label_color = "black"
        response_box_outline = "black"
        response_box_fill = "gray"

    # thickness of outline around response box
    outline_thickness_px = 6

    response_button_width = (screen_width/6) # based on size in previous experiments
    response_button_height = screen_height/2
    response_left_x = 0 - (screen_width/2) + (response_button_width/2)
    response_right_x = 0 + (screen_width/2) - (response_button_width/2)
    response_height = 0 + (screen_height/2) - (response_button_height/2)

    button_label_font_size = button_size

    button_left = visual.Rect(win,fillColor=response_box_fill,lineWidth=outline_thickness_px,lineColor=response_box_outline,width=response_button_width,height=response_button_height,pos=[response_left_x,response_height])
    button_right = visual.Rect(win,fillColor=response_box_fill,lineWidth=outline_thickness_px,lineColor=response_box_outline,width=response_button_width,height=response_button_height,pos=[response_right_x,response_height])
    button_left_label = visual.TextStim(win,text="Change",color=response_label_color,height=button_label_font_size,pos=[response_left_x,response_height])
    button_right_label = visual.TextStim(win,text="No\nChange",color=response_label_color,height=button_label_font_size,pos=[response_right_x,response_height])
    button_left.draw()
    button_right.draw()

    button_left_label.draw()
    button_right_label.draw()

    return(button_left,button_right)

def drawResponseButtonsAnywhere(button_size,screen_width,screen_height,leftLocs,rightLocs):
    DEBUG_CODE = 1

    if(DEBUG_CODE):
        response_label_color = "white"
        response_box_outline = "black"
        response_box_fill = "black"
    else:
        response_label_color = "black"
        response_box_outline = "black"
        response_box_fill = "gray"

    outline_thickness_px = 6

    response_button_width = (screen_width/6) # based on size in previous experiments
    response_button_height = screen_height/2

    button_label_font_size = button_size

    button_left = visual.Rect(win,fillColor=response_box_fill,lineWidth=outline_thickness_px,lineColor=response_box_outline,width=response_button_width,height=response_button_height,pos=[leftLocs[0],leftLocs[1]])
    button_right = visual.Rect(win,fillColor=response_box_fill,lineWidth=outline_thickness_px,lineColor=response_box_outline,width=response_button_width,height=response_button_height,pos=[rightLocs[0],rightLocs[1]])
    button_left_label = visual.TextStim(win,text="Change",color=response_label_color,height=button_label_font_size,pos=[leftLocs[0],leftLocs[1]])
    button_right_label = visual.TextStim(win,text="No\nChange",color=response_label_color,height=button_label_font_size,pos=[rightLocs[0],rightLocs[1]])
    button_left.draw()
    button_right.draw()
    button_left_label.draw()
    button_right_label.draw()

# ----------------------------------------------------------------------------
# RUN BLOCK FUNCTION
# ----------------------------------------------------------------------------

def runBlock(block_num, block_structure, timeout_duration, filename, data_file):
    BLOCK = block_num
    TRIAL = 1

    # one for change
    # one for no change
    # one for general grid list
    # defined each block
    change_target_grid_list = list(mygrid)
    nochange_target_grid_list = list(mygrid)

    while(TRIAL <= len(block_structure)):
        mymouse = event.Mouse(visible=False)

        # get trial data
        trial_data_ = block_structure[TRIAL-1]
        trial_data = trial_data_.split("_")
        setSize = int(float(trial_data[1]))
        trial_type = trial_data[0]

        # defines if change_trial
        if(trial_type == "change"):
            isChangeTrial = 1
        elif(trial_type == "noChange"):
            isChangeTrial = 0

        # get trial colors
        # random sample full list, any extras needed, grab copy of original list, and repeats
        trial_colors = colors2sample(setSize,colors)
        shuffle(trial_colors)

        # draw fixation
        bLeft,bRight = drawResponseButtons(36,screen_width,screen_height)
        drawFixation(6)
        win.flip()
        core.wait(fixation_duration)

        # draw initial display
        # --------------------------------
        bLeft,bRight = drawResponseButtons(36,screen_width,screen_height)
        win.flip()
        core.wait(blank_duration)

        # define new grid list
        grid_list = list(mygrid)

        # generate first set of stimuli
        # --------------------------------
        # shuffle lists
        shuffle(change_target_grid_list)
        shuffle(nochange_target_grid_list)
        shuffle(grid_list)

        # define list of locations for second drawing
        replay_list = list()

        # draw all distractors
        for color in trial_colors[:-1]:
            if(len(trial_colors) > len(grid_list)):
                print "ERROR: MORE COLORS THAN GRID ELEMENTS"
                core.quit()
            grid_element = grid_list.pop()
            next_list = grid_element
            replay_list.append(next_list)
            obj = ChangeSquare([grid_element[0],grid_element[1]],"",color,"D",isChangeTrial*0,SQUARE_SIZE)
            obj.stim.draw()
            EXPORT_DATA = [str(BLOCK),str(TRIAL),trial_data_,obj.identity,str(obj.position[0]),str(obj.position[1]),obj.color,str(obj.isChangeTrial)]
            writeData(filename,"a",EXPORT_DATA)

        # draw target
        if(isChangeTrial):
            grid_element = change_target_grid_list.pop()
            if(grid_element not in grid_list):
                #print "not in list"
                change_target_grid_list.append(grid_element)
                grid_element = change_target_grid_list.pop()
        else:
            grid_element = nochange_target_grid_list.pop()
            if(grid_element not in grid_list):
                #print "not in list"
                nochange_target_grid_list.append(grid_element)
                grid_element = nochange_target_grid_list.pop()

        Targ_x = grid_element[0]
        Targ_y = grid_element[1]
        TARG_START_COLOR = trial_colors[-1]
        next_list = grid_element
        replay_list.append(next_list)
        obj = ChangeSquare([grid_element[0],grid_element[1]],"",trial_colors[-1],"T",isChangeTrial*0,SQUARE_SIZE)
        obj.stim.draw()

        bLeft,bRight = drawResponseButtons(36,screen_width,screen_height)
        win.flip()
        core.wait(stimulus_duration)

        EXPORT_DATA = [str(BLOCK),str(TRIAL),trial_data_,obj.identity,str(obj.position[0]),str(obj.position[1]),obj.color,str(obj.isChangeTrial)]
        writeData(filename,"a",EXPORT_DATA)

        lenFullGridCheck = len(grid_list) + setSize - 1

        # reverse indices because of how they were popped out last first and copy it
        reverse_list = list(reversed(replay_list))
        rcopy = list(reverse_list)
        shuffle(rcopy)

        # if change trial, change one color
        if(isChangeTrial):
            popped_color = trial_colors.pop()
            chosen_color = choice(colors)
            while(chosen_color == popped_color):
                chosen_color = choice(colors)
            trial_colors.append(chosen_color)

        # generate second set of stimuli
        # --------------------------------
        # draw all distractors
        obj_list = list()
        obj_idens = list()
        for color in trial_colors[:-1]:
            if(len(trial_colors) > len(grid_list)):
                print "ERROR: MORE COLORS THAN GRID ELEMENTS"
                core.quit()
            grid_element = reverse_list.pop()
            obj = ChangeSquare([grid_element[0],grid_element[1]],"",color,"D",isChangeTrial,SQUARE_SIZE)
            obj_list.append(obj.stim)
            obj_idens.append(obj.identity)
            #obj.stim.draw()
            EXPORT_DATA = [str(BLOCK),str(TRIAL),trial_data_,obj.identity,str(obj.position[0]),str(obj.position[1]),obj.color,str(obj.isChangeTrial)]
            writeData(filename,"a",EXPORT_DATA)

        # draw target
        TARG_END_COLOR = trial_colors[-1]
        grid_element = reverse_list.pop()
        obj = ChangeSquare([Targ_x,Targ_y],"",trial_colors[-1],"T",isChangeTrial,SQUARE_SIZE)
        obj_list.append(obj.stim)
        obj_idens.append(obj.identity)
        #obj.stim.draw()

        EXPORT_DATA = [str(BLOCK),str(TRIAL),trial_data_,obj.identity,str(obj.position[0]),str(obj.position[1]),obj.color,str(obj.isChangeTrial)]
        writeData(filename,"a",EXPORT_DATA)

        # draw nothing - 900 ms
        # --------------------------------
        bLeft,bRight = drawResponseButtons(36,screen_width,screen_height)
        win.flip()
        core.wait(intertrial_interval)
        # --------------------------------

        # wait up to 2200 ms for a response
        # --------------------------------
        start_time = clock()

        ResponseGiven = False
        elapsed = clock() - start_time
        mymouse.getPos()
        while(ResponseGiven == False and elapsed < timeout_duration):
            drawObjList(obj_list)
            bLeft,bRight = drawResponseButtons(36,screen_width,screen_height)
            response_ids = ["change","noChange"]
            response_list = [bLeft,bRight]
            win.flip()
            elapsed = clock() - start_time
            if(elapsed > timeout_duration):
                isObjTarget = "NA"
                isTimeoutTrial = 1
                end_time = clock()
                Click_X = "NA"
                Click_Y = "NA"
                #print "x: " + Click_X + " y: " + Click_Y
                ResponseGiven = True
            else:
                mouse1, mouse2, mouse3 = mymouse.getPressed()
                if(mouse1):
                    isObjTarget = response_ids[0]
                    #print("noChange")
                    isTimeoutTrial = 0
                    end_time = clock()
                    mouse_pos = mymouse.getPos()
                    Click_X = mouse_pos[0]
                    Click_Y = mouse_pos[1]
                    ResponseGiven = True
                elif(mouse3):
                    isObjTarget = response_ids[1]
                    #print("change")
                    isTimeoutTrial = 0
                    end_time = clock()
                    mouse_pos = mymouse.getPos()
                    Click_X = mouse_pos[0]
                    Click_Y = mouse_pos[1]
                    ResponseGiven = True
                else:
                    continue

        if(end_time == None):
            isTimeoutTrial = 1
            end_time = clock()
            Click_X = "NA"
            Click_Y = "NA"
            ResponseGiven = False

        # calculate RT
        RT = end_time - start_time

        # check if object clicked
        try:
            isObjTarget
        except NameError:
            isObjTarget = "NA"

        # save trial data
        tdata = Data(BLOCK,TRIAL,trial_type,setSize,RT,Click_X,Click_Y,Targ_x,Targ_y,TARG_START_COLOR,TARG_END_COLOR,isObjTarget,isTimeoutTrial)
        writeDataString(data_file,"a",tdata.genWriteString())

        isObjTarget = None

        TRIAL += 1
    VALID_RUN = 1
    return(VALID_RUN)

# ===========================================================================================================
# ========================================= EXPERIMENT CONFIGURATION ========================================
# ===========================================================================================================

# ----------------------------------------------------------------------------
# READ CONFIG PARAMETERS
# ----------------------------------------------------------------------------

# to get data from a variable in the config filename
# make sure the input data looks like name:value|type <------- NO SPACES
# ConfigData("name_of_var_in_config_file).getValue()

# create config objects
DEBUG_CODE = ConfigData("debug").getValue()

# ----------------------------------------------------------------------------
# SCREEN PARAMETERS
# ----------------------------------------------------------------------------
# determine if monitor is 16:9 aspect ratio of 4:3
# if 16:9, use is_widescreen = 1
# else, use is_widescreen = 0
isWidescreen = ConfigData("isWidescreen").getValue()
isRetina = ConfigData("isRetina").getValue()

screen_width = ConfigData("screen_width").getValue()
screen_height = ConfigData("screen_height").getValue()

if(isRetina):
    # get screen resolution (dimensions: px)
    screen_width = screen_width/2
    screen_height = screen_height/2
else:
    screen_width = screen_width
    screen_height = screen_height

# define square size and buffers relative to it
SQUARE_SIZE = ConfigData("square_size").getValue()
BUFFER_CONTROLLER = ConfigData("buffer_controller").getValue()
WINDOW_BUFFER_CONTROLLER = ConfigData("window_buffer_controller").getValue()
buffer = SQUARE_SIZE/BUFFER_CONTROLLER
window_buffer = (SQUARE_SIZE * WINDOW_BUFFER_CONTROLLER)

# screen color
screen_bgColor = ConfigData("screen_bgColor").getValue()

# ----------------------------------------------------------------------------
# INSTRUCTION PARAMETERS
# ----------------------------------------------------------------------------

headline_text = "INSTRUCTIONS"
headline_height_adj = ConfigData("heading_font_height_adj").getValue()
headline_height = screen_height/headline_height_adj
current_instruct = ''
instruct_height_adj = ConfigData("instruct_font_height_adj").getValue()
instruct_height = screen_height/instruct_height_adj
font_color = ConfigData("fontColor").getValue()

# ----------------------------------------------------------------------------
# EXPERIMENT PARAMETERS
# ----------------------------------------------------------------------------

if(DEBUG_CODE == 1):
    # define timing parameters
    fixation_duration = .001
    stimulus_duration = .001
    blank_duration = .001
    intertrial_interval = .001
    timeout_duration = .001
else:
    # define timing parameters
    fixation_duration = ConfigData("fixation_duration").getValue()
    stimulus_duration = ConfigData("stimulus_duration").getValue()
    blank_duration = ConfigData("blank_duration").getValue()
    intertrial_interval = ConfigData("intertrial_interval").getValue()
    timeout_duration = ConfigData("timeout_duration").getValue()

# define colors used in experiment
colors = ConfigData("square_colors").getValue()

# get 6x6 grid with 700px usable_x by usable_y space
mygrid = getGridLocations(screen_height,screen_width,buffer,window_buffer,isWidescreen)
if(len(mygrid) != 36):
    print "ERROR: incorrect grid cell count", len(mygrid)
    df = open("grid_locs.txt","w")
    df.write("x"+"\t"+"y"+"\n")
    for gi in mygrid:
        df.write(str(gi[0]) + "\t" + str(gi[1]) + "\n")
    df.close()
    core.quit()

# ----------------------------------------------------------------------------
# PARTICIPANT PARAMETERS
# ----------------------------------------------------------------------------

# get participant info
if(DEBUG_CODE == 1 or DEBUG_CODE == 2):
    subject_number = 999
else:
    subject_number = my_gui()
print subject_number
subject_parity = getSubjectInfo(subject_number)

# ----------------------------------------------------------------------------
# FOR PSYCHOPY ONLY
# ----------------------------------------------------------------------------

# define experiment window
if(DEBUG_CODE == 1):
    win = visual.Window(color=screen_bgColor, units="pix",size=[screen_width,screen_height])
elif(DEBUG_CODE == 2):
    win = visual.Window(color=screen_bgColor, units="pix",size=[screen_width,screen_height])
else:
    win = visual.Window(color=screen_bgColor, units="pix",fullscr=True)

if(DEBUG_CODE == 2):
    # draw test grid to count location
    for i in mygrid:
        grid_element = i
        obj = ChangeSquare([grid_element[0],grid_element[1]],"","black","NA",1,SQUARE_SIZE)
        obj.stim.draw()

    win.flip()
    k=['']
    while(k[0] not in ['escape','esc','space']):
        k = event.waitKeys()

# ----------------------------------------------------------------------------
# GENERATE FILE NAMES
# ----------------------------------------------------------------------------

# generate filenames for participant
filename = "obj/exp/8/objdata" + "_" + str(subject_number) + ".txt"
data_file = "data/exp/8/data" + "_" + str(subject_number) + ".txt"

# write file header for object list
EXPORT_DATA_HEADER = ["block","trial","trial_type","obj_identity","x","y","obj.color","isChangeTrial"]
writeData(filename,"w",EXPORT_DATA_HEADER)

# write file header for data file
EXPORT_DATA_HEADER = ["datetime","block","trial","trial_type","setSize","RT","accuracy","timeout","clickedObject","Targ_X","Targ_Y","Click_X","Click_Y","target_start_color","target_end_color"]
writeData(data_file,"w",EXPORT_DATA_HEADER)

# ----------------------------------------------------------------------------
# DEFINE ALL EXPERIMENTAL BLOCKS
# ----------------------------------------------------------------------------

# define trial types
trials_types = ["change","noChange"]

# define number of trials per trial type
if(DEBUG_CODE == 1 or DEBUG_CODE == 2):
    NUM_PRACTICE_TRIALS_PER_CONDITION = ConfigData("numPracticeTrialsCondition").getValue()
    TRIALS_PER_MINIBLOCK = 4
else:
    NUM_PRACTICE_TRIALS_PER_CONDITION = ConfigData("numPracticeTrialsCondition").getValue()
    TRIALS_PER_MINIBLOCK = ConfigData("numExpTrialsCondition").getValue()

# ----------------------------------------------------------------------------
# RUN ALL BLOCKS OF EXPERIMENT
# ----------------------------------------------------------------------------

if DEBUG_CODE == 0 or DEBUG_CODE == 2:
    # instructions
    instructs_list = ConfigData("exp_instruct_list").getValue()
    INSTRUCTS = Instructions(headline_text,headline_height,current_instruct,instructs_list,instruct_height,font_color)
    INSTRUCTS.drawAll()

    # last value determines if to return randomized list or not (1 = yes)
    block_data = genBlock(TRIALS_PER_MINIBLOCK,8,trials_types,1)

    # run the practice block
    runBlock(1, block_data, timeout_duration, filename, data_file)
