% Clear the workspace
%close all;
%clearvars;
%sca;

% Setup PTB with some default values
PsychDefaultSetup(2);

% Seed the random number generator. Here we use the an older way to be
% compatible with older systems. Newer syntax would be rng('shuffle'). Look
% at the help function of rand "help rand" for more information
rand('seed', sum(100 * clock));

% Set the screen number to the external secondary monitor if there is one
% connected
screenNumber = max(Screen('Screens'));

% Define black, white and grey
white = WhiteIndex(screenNumber);
grey = white / 2;
black = BlackIndex(screenNumber);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% imports of any libraries, etc
% Screen('Preference', 'SkipSyncTests', 1);

% for cross-platform key identification
KbName('UnifyKeyNames');

% get time to wait for keypresses
WaitTime = 0.017;

% set experiment totaltime (seconds)
ExpTotalTime = 300;

% release all events in the event queue
FlushEvents; 
while KbCheck; end

% Get user input
prompt = {'Participant ID#:','Session #:'};
dlg_title = 'Input';
num_lines = 1;
defaultans = {'DEBUG','DEBUG'};
answer = inputdlg(prompt,dlg_title,num_lines,defaultans);

% extract from input dlg
participant = answer(1);
project = answer(2);

disp('-------------------------------');
disp('Experiment STARTED');
disp('-------------------------------');
disp(['Participant: ' participant]);
disp(['Project: ' project]);

HideCursor();

% experiment data files location and file type
data_path = 'data/';
file_ext = '.csv';

% create filename
filename = strjoin([data_path,'data_',participant,file_ext],'');

% get the current date
thedate = date;

% release all events in the event queue
keyIsDown = 0;
FlushEvents; 
while KbCheck; end

% create 0x0 cell array
UserData = {};

% initialize event counter
eventCounter = 0;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% WINDOW INIT
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Open the screen
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, grey, [], 32, 2);

% Flip to clear
Screen('Flip', window);

% Query the frame duration
ifi = Screen('GetFlipInterval', window);

% Set the text size
Screen('TextSize', window, 30);

% Query the maximum priority level
topPriorityLevel = MaxPriority(window);

% Get the centre coordinate of the window
[xCenter, yCenter] = RectCenter(windowRect);

% Set the blend funciton for the screen
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% DISPLAY INSTRUCTIONS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

DrawFormattedText(window, 'Thought Monitoring \n\n Hold the spacebar during the time you are thinking a thought specified by your experimenter.\n\nRelease the spacebar key when you are no longer thinking this thought.\n\nThe entire experiment will last for 5 minutes.',...
    'center', 'center', black);
Screen('Flip', window);
KbStrokeWait;

% clear the window after drawing instructions
DrawFormattedText(window, '',...
    'center', 'center', black);
Screen('Flip', window);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

commandwindow;

% get experiment start time
ExpStartTime = GetSecs;

while (GetSecs < (ExpStartTime + ExpTotalTime))
    % get start time for this trial
    TrialStartTime = GetSecs; 

    RemainingWait = ExpTotalTime - (GetSecs - ExpStartTime);

    % while experimentRunning
    while (GetSecs < (TrialStartTime + WaitTime))

        [keyIsDown, secs_press, key_pressed] = KbCheck; % this will keep checking the keyboard until Waittime is exceeded
        if keyIsDown % if a key is pressed figure out what it was and when it was

            [secs_release, key_released, deltaSecs] = KbReleaseWait;
            response_press = KbName(key_pressed);
            response_release = KbName(key_released);
            holdDuration = secs_release-secs_press;
            press_relative_trial_start = secs_press - TrialStartTime; 
            press_relative_exp_start = secs_press - ExpStartTime;

            % release all events in the event queue
            keyIsDown = 0;
            FlushEvents;

            % increment event counter
            eventCounter = eventCounter + 1;

            UserData{eventCounter,1} = participant;
            UserData{eventCounter,2} = project;
            UserData{eventCounter,3} = thedate;
            UserData{eventCounter,4} = ExpStartTime;
            UserData{eventCounter,5} = eventCounter;
            UserData{eventCounter,6} = secs_press;
            UserData{eventCounter,7} = secs_release;
            UserData{eventCounter,8} = holdDuration;
            UserData{eventCounter,9} = press_relative_trial_start;
            UserData{eventCounter,10} = press_relative_exp_start;
            UserData{eventCounter,11} = filename;

            % this means you break out of the while loop 
            % so you don't wait any longer after key is pressed
            break 
        else % if no key was pressed
            FlushEvents;
        end
    end
end

% get experiment end time
ExpEndTime = GetSecs;

if(not(isempty(UserData)))
    TrialTable = cell2table(UserData, 'VariableNames',{'participant','project','date','exp_start_time','trial','key_press_time','key_release_time','keyhold_duration','presstime_relative_trial_start','presstime_relative_exp_start','filename'});
    TrialTable.press_time_relative_exp_end = ExpEndTime - TrialTable.key_press_time;
    TrialTable.release_time_relative_exp_end = ExpEndTime - TrialTable.key_release_time;
%    TrialTable.exp_end_time = ExpEndTime;
    writetable(TrialTable,filename);
else
    UserData = {participant,project,thedate,ExpStartTime,'NA','NA','NA','NA','NA','NA','NA'};
    TrialTable = cell2table(UserData, 'VariableNames',{'participant','project','date','exp_start_time','trial','key_press_time','key_release_time','keyhold_duration','presstime_relative_trial_start','presstime_relative_exp_start','filename'});
    TrialTable.press_time_relative_exp_end = 'NA';
    TrialTable.release_time_relative_exp_end = 'NA';
    TrialTable.exp_end_time = ExpEndTime;
    writetable(TrialTable,filename);
end

disp('-------------------------------');
disp('EXPERIMENT COMPLETE');
disp('-------------------------------');
totalTime = (ExpEndTime - ExpStartTime);
disp(['Total Run Time (seconds):']);
disp([totalTime]);
disp('-------------------------------'); 

DrawFormattedText(window, ['The experiment is now complete'],...
    'center', 'center', black);
Screen('Flip', window);
KbStrokeWait;

sca;