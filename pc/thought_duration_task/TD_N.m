% ----------------------------------------
% THOUGHT DURATION PARADIGM
% developed by: Nelson Roque (roque@psy.fsu.edu)
% ----------------------------------------
% last modified: 5/3/17 | 12:53 PM
% ----------------------------------------

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% SCRIPT PREPARATION
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Clear the workspace for memory management purposes
close all;
clearvars;
sca;

% for debugging only
Screen('Preference','SkipSyncTests', 1);

% Setup PTB with some default values
PsychDefaultSetup(2);

% Seed the random number generator. Here we use the an older way to be
% compatible with older systems. Newer syntax would be rng('shuffle'). Look
% at the help function of rand "help rand" for more information
rand('seed', sum(100 * clock));

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% EXPERIMENTAL PARAMETERS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% experiment total time (300 seconds)
Total_Exp_Time = 15.0000;

% get the current date
thedate = date;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% PARTICIPANT INFO GUI
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Get user input
prompt = {'ParticipantID_SessionID:','SessionID (for redundancy)'};
dlg_title = 'Input';
num_lines = 1;
defaultans = {'DEBUG','DEBUG'};
answer = inputdlg(prompt,dlg_title,num_lines,defaultans);

% extract from input dlg
participant = answer(1);
session = answer(2);

% write to the console
% participant information
disp('-------------------------------');  % disp(), display contents in the command window
disp('PARTICIPANT INFORMATION');
disp('-------------------------------');
disp(['Participant: ' participant]);
disp(['Session: ' session]);

% experiment data files location and file type
data_path = 'data/';
file_ext = '.csv';

% create filename
filename = strjoin([data_path,'data_',participant,'-session_',session,file_ext],''); % strjoin(C, delimiter) join strings with a 'delimiter' in between

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%KEYBOARD INIT
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% for cross-platform key identification
KbName('UnifyKeyNames');

% release all events in the event queue
FlushEvents; 
while KbCheck; end % KbCheck and KbWait are MEX files, which takes time to load when they are first called. They will stay loaded until you flush them.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% WINDOW INIT
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Set the screen number to the external secondary monitor if there is one
% connected
screenNumber = max(Screen('Screens'));

% Define black, white and grey
white = WhiteIndex(screenNumber); %WhiteIndex(), find the color value in the current screen depth. = 1
grey = white / 2; % = .5
black = BlackIndex(screenNumber); % = 0

% Open the screen
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, grey, [], 32, 2); % ? not sure about 32 and 2

% Flip to clear
Screen('Flip', window);

% Query the frame duration
ifi = Screen('GetFlipInterval', window); % ifi = .0167

% set as time to wait for keypresses
WaitTime = ifi;

% Set the text size
Screen('TextSize', window, 30);

% Query the maximum priority level
topPriorityLevel = MaxPriority(window);

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Set the blend funciton for the screen
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% START THE EXPERIMENT (INSTRUCTIONS + SETUP)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% hide the cursor to not distract the participant
HideCursor();

% first set of instructions
DrawFormattedText(window, 'Thought Monitoring \n\n Hold the spacebar during the time you are thinking a thought specified by your experimenter.\n\nRelease the spacebar key when you are no longer thinking this thought.\n\nThe entire experiment will last for 5 minutes.',...
    'center', 'center', black);
Screen('Flip', window);
KbStrokeWait; % wait for a single keystroke of the subject

% clear the window after drawing instructions
DrawFormattedText(window, '',...
    'center', 'center', black);
Screen('Flip', window);

% insert wait buffer for screen flip
WaitSecs(2);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% COLLECT THE DATA
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% create 0x0 cell array
UserData = {};

% initialize the trial counter
Trial_Index = 1;

% get the start of the experiment
StartTime_Exp = GetSecs;

while ((GetSecs - StartTime_Exp) < Total_Exp_Time)
    % get the start of the trial
    StartTime_Trial = GetSecs;
    
    % wait for key press
    [secs_1, key_1, delta_1] = KbWait([],0,(StartTime_Exp + Total_Exp_Time));
    Key_Press_Time = GetSecs;
    
    % wait for key release
    [secs_2, key_2, delta_2] = KbWait([],1,(StartTime_Exp + Total_Exp_Time));
    Key_Release_Time = GetSecs;
    
    % calculate hold time
    Key_Hold_Duration = Key_Release_Time - Key_Press_Time;
   
    % calculate press and release, relative to experiment start
    Key_Press_Relative_Exp_Start = Key_Press_Time - StartTime_Exp;
    Key_Release_Relative_Exp_Start = Key_Release_Time - StartTime_Exp;
   
    % log all data to cell array for later writing to csv
    UserData{Trial_Index,1} = participant;
    UserData{Trial_Index,2} = filename;
    UserData{Trial_Index,3} = session;
    UserData{Trial_Index,4} = thedate;
    UserData{Trial_Index,5} = Trial_Index;
    UserData{Trial_Index,6} = StartTime_Exp;
    UserData{Trial_Index,7} = 0;
    UserData{Trial_Index,8} = StartTime_Trial;
    UserData{Trial_Index,9} = Key_Press_Time;
    UserData{Trial_Index,10} = Key_Release_Time;
    UserData{Trial_Index,11} = Key_Hold_Duration;
    UserData{Trial_Index,12} = Key_Press_Relative_Exp_Start;
    UserData{Trial_Index,13} = Key_Release_Relative_Exp_Start;

    % increment trial counter
    Trial_Index = Trial_Index + 1;
end

% get the end of the experiment timestamp
EndTime_Exp = GetSecs;

% calculate total experiment time
TotalTime_Exp = EndTime_Exp - StartTime_Exp;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% SAVE THE DATA
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if(not(isempty(UserData)))
    % convert the cell array to a table for easy column appending
    TrialTable = cell2table(UserData, 'VariableNames',{'participant','filename','session','date','trial','start_time_exp','end_time_exp','start_time_trial','key_press_time','key_release_time','key_hold_duration','key_press_relative_exp_start','key_release_relative_exp_start'});
    
    % get experiment end time into the data frame
    TrialTable.end_time_exp = TrialTable.end_time_exp + EndTime_Exp;
    
    % calculate key presses, relative to the end of the experiment
    TrialTable.key_press_relative_exp_end = TrialTable.end_time_exp - TrialTable.key_press_time;
    TrialTable.key_release_relative_exp_end = TrialTable.end_time_exp - TrialTable.key_release_time;
    
    % write the data to a csv file
    writetable(TrialTable,filename);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% CLOSEOUT THE EXPERIMENT
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Echo message to participant that task is now complete
DrawFormattedText(window, ['The experiment is now complete'],...
    'center', 'center', black);
Screen('Flip', window);
WaitSecs(2); 

sca;

% write to the console
% that the experiment is now complete
disp('-------------------------------');
disp('EXPERIMENT COMPLETE');
disp('-------------------------------');
disp(['Total Run Time (seconds):']);
disp(TotalTime_Exp);
disp('-------------------------------'); 