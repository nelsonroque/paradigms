%--------------------------------------------------------------------------
% PP CODE IS TEMPORARILY COMMENTED OUT. UNDO THIS FOR THE REAL VERSION
%--------------------------------------------------------------------------
% CLEAR ALL, CLOSE ALL, COMMANDWINDOW ARE ALL ACTIVE. COMMENT THESE OUT FOR
% THE REAL VERSION
%--------------------------------------------------------------------------

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
% IN THIS VERSION, EACH PARTICIPANT GETS A SINGLE TARGET TO SEARCH FOR, 
% FOR THE ENTIRE EXPERIMENT, IE, ACROSS ALL BLOCKS.                         
% -------------------------------------------------------------------------
% THE TARGET IS DETERMINED BY COMPUTATIONS PERFORMED ON THE SUBJECT NUMBER
% -------------------------------------------------------------------------
% THE NUMBER OF TEXTURES HAS BEEN REDUCED TO 8. THEY'RE CALLED FROM THE
% TEXTURE_WB VARIABLE
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 

function CMP300()
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% HOUSEKEEPING, FOR EFFICIENCY
% -------------------------------------------

% clear workspace 
clear all;
% 
% % clear command window
clc;
% 
% % moves to the command window so KB input doesnt enter code itself
commandwindow;

total_subs = 1;

for subi=1:total_subs
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% EXPERIMENT & PROBABILITY PARAMETERS
% -------------------------------------------
% comment out the line below before experimentation
Screen('Preference', 'SkipSyncTests', 1);

% set random seed
RandStream.setGlobalStream(RandStream('mt19937ar','seed',sum(100*clock))); % reset the random seed

% debug code (0 = normal, 1 = fake run through)                    
DEBUG_CODE = 1;

% set stimuli image folder
IMG_Folder = 'images/';

% set possible participant dimensions
part_dimensions = ['H','V']; % horizontal, vertical

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% GET PARTICIPANT VARIABLES (WITH GUI)
% -------------------------------------------

% Open GUI Window for participant input
if DEBUG_CODE == 0
    prompt = {'Participant Number:' 'Participant Initials'};
    dlg_title = 'New Participant';
    num_lines = 1;
    defAns = {'0' '0' '0' '0'};
    answer = inputdlg(prompt,dlg_title,num_lines,defAns);
    
    % if cancel is pressed, listen for an empty cell array
    if isempty(answer)
        answer = {'0' '0' '0' '0'};  
        part_num = num2str(round(GetSecs));
        part_initials = 'USER_PRESSED_CANCEL';
    else % if input is received, store values 
        part_num = answer{1};
        part_initials = answer{2};
    end
else
    part_num = '7';
    part_initials = 'DEBUGGING';
end

% dynamically get date/time (dependent on computer clock)
% double-check for their accuracy
cur_date = date;
cur_time = datestr(now, 'HH:MM:SS');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

numTargets=8;
part_num = str2double(part_num);

if mod((part_num/numTargets),1) == .125 | mod((part_num/numTargets),1) == .250
    firstBlock = '1';
elseif mod((part_num/numTargets),1) == .375 | mod((part_num/numTargets),1) == .5
    firstBlock = '3';
elseif mod((part_num/numTargets),1) == .625 | mod((part_num/numTargets),1) == .75
    firstBlock = '7';
elseif mod((part_num/numTargets),1) == .875 | mod((part_num/numTargets),1) == 0
    firstBlock = '9';
end

% trial count, to create probability distribution
exp_trial_count = 300;
percentage_practice = .10;
practice_count = exp_trial_count * percentage_practice;

% create probability structure
num_nt_conditions = 7;
prob_target = 15;
prob_non_target = (100 - prob_target);
prob_nt_each = (prob_non_target/num_nt_conditions);

% get number of trials of each for exp
targ_var_exp = (exp_trial_count * prob_target)/100;
nontarg_var_exp = (exp_trial_count * prob_nt_each)/100;
target_trials_exp = round(targ_var_exp);
nontarg_trials_exp = round(nontarg_var_exp);

% get number of trials of each for practice
targ_var_prac = (practice_count * prob_target)/100;
nontarg_var_prac = (practice_count * prob_nt_each)/100;
target_trials_prac = round(targ_var_prac);
nontarg_trials_prac = round(nontarg_var_prac);

% get block number
Curr_Block_Num = [0 1 2 3 4 5];
Block0 = Curr_Block_Num(1);
Block1 = Curr_Block_Num(2);
Block2 = Curr_Block_Num(3);
Block3 = Curr_Block_Num(4);
Block4 = Curr_Block_Num(5);
Block5 = Curr_Block_Num(6);

% CREATE PROBABILITY DISTRIBUTION
% -------------------------------------------
% initialize distribution list to be
% length of target trials, of zeros
block_distribution_exp = ones(target_trials_exp,1);
block_distribution_prac = ones(target_trials_prac,1);

% create number of non-target trials 
% ---
% since each dimension has equal probability
% can create array all in one go
% ---
% you would need a seperate while block
% if you want to change individual probabilities
i = 0;
while (i < nontarg_trials_exp)
    block_distribution_exp(end + 1) = 2;
    block_distribution_exp(end + 1) = 3;
    block_distribution_exp(end + 1) = 4;
    block_distribution_exp(end + 1) = 5;
    block_distribution_exp(end + 1) = 6;
    block_distribution_exp(end + 1) = 7;
    block_distribution_exp(end + 1) = 8;
    i = i + 1;
end

% create block distribution for practice
i = 0;
while (i < nontarg_trials_prac)
    block_distribution_prac(end + 1) = 2;
    block_distribution_prac(end + 1) = 3;
    block_distribution_prac(end + 1) = 4;
    block_distribution_prac(end + 1) = 5;
    block_distribution_prac(end + 1) = 6;
    block_distribution_prac(end + 1) = 7;
    block_distribution_prac(end + 1) = 8;
    i = i + 1;
end

% columns needed in cell array for holding stimuli database
varsNeeded = 17;

% STIMULI PRESENTATION PARAMETERS
% -------------------------------------------
% set stimulus presentation variables
if DEBUG_CODE == 0
    STIM_DURATION = .5;
    STIM_DUR = STIM_DURATION;
    ISI = 1.5;
else
    STIM_DURATION = .01;
    STIM_DUR = STIM_DURATION;
    ISI = .01;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% CREATE DYNAMIC PARTICIPANT FILE (one for each participant)
% -------------------------------------------
part_num = num2str(part_num);

dataFolder = 'data/Participant_';
dataSuffix = '.txt';
dataFile = cat(2,dataFolder,part_num);
dataFile = cat(2,dataFile,dataSuffix);

% open the data file
inputFile = fopen(dataFile, 'a+');

% write header
fprintf(inputFile, 'Participant\tpart_initials\tdate\ttime\tBlockTarg');
fprintf(inputFile, '\tBlockNum\tTrial\tisPractice\tAbsPosition\tFileName');
fprintf(inputFile, '\tSearchType\tRelevance\tStepsDim\tEEG_code\tAxis\tRT\tAccuracy\n');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% CUSTOMIZE EXPERIMENT BASED ON SUBJECT PARITY
% -------------------------------------------
% if part_num = odd, then horizontal dimension
% if part_num = even, then vertical dimension
if mod(part_num,2)
   part_dimension = 'H';
else
   part_dimension = 'V';
end

% based on dimension, assign a block condition matrix
% (target|relevant1|relevant2|irrelevant1|irrelevant2|rel2irrel1,irrel2rel1)
if (part_dimension == 'V')
    block_condition_matrix = ['1','2','3','4','7','6','8','9' ; '3','2','1','6','9','4','8','7'; '7','8','9','4','1','6','2','3'; '9','8','7','6','3','4','2','1']; 
else
    block_condition_matrix = ['1','4','7','2','3','8','6','9'; '3','6','9','2','1','8','4','7'; '7','4','1','8','9','2','6','3'; '9','6','3','8','7','2','4','1']; 
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% SCREEN SETUP
% -------------------------------------------
% get screens, and screen center
screens = Screen('Screens');
dispScreen = max(screens);
  
% non fullscreen window for debugging purposes
% allows you to still see the command window and look for error messages
% [MyScreen, rect] = Screen('OpenWindow', dispScreen, [], [500 350 640 480]);

% for experiment
[MyScreen, rect] = Screen('OpenWindow', dispScreen, [24 64 112]);

     
Screen('TextFont',MyScreen,'-sony-fixed-medium-r-normal--24-230-75-75-c-120-iso8859-1');

% do final screens setup
% screen stuff
[screenXpixels, screenYpixels] = Screen('WindowSize', MyScreen);
[xCenter, yCenter] = RectCenter(rect);

% adjust fixation cross distance from (center, center)
v_spacing = 12;
h_spacing = 9;

% hide cursor from participants
HideCursor;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% CREATE STIM DATABASE FOR EACH BLOCK (INCLUDING PRACTICE)
% -------------------------------------------
[block_1_stimuli_db, Texture_WB] = block_distribution_creator(block_distribution_exp,block_condition_matrix,firstBlock,varsNeeded,part_dimension,IMG_Folder,MyScreen,'NP',xCenter,yCenter, Block0);
[block_1p_stimuli_db, Texture_WB] = block_distribution_creator(block_distribution_prac,block_condition_matrix,firstBlock,varsNeeded,part_dimension,IMG_Folder,MyScreen,'P',xCenter,yCenter, Block1);
[block_2_stimuli_db, Texture_WB] = block_distribution_creator(block_distribution_exp,block_condition_matrix,firstBlock,varsNeeded,part_dimension,IMG_Folder,MyScreen,'NP',xCenter,yCenter, Block2);
[block_3_stimuli_db, Texture_WB] = block_distribution_creator(block_distribution_exp,block_condition_matrix,firstBlock,varsNeeded,part_dimension,IMG_Folder,MyScreen,'NP',xCenter,yCenter, Block3);
[block_4_stimuli_db, Texture_WB] = block_distribution_creator(block_distribution_exp,block_condition_matrix,firstBlock,varsNeeded,part_dimension,IMG_Folder,MyScreen,'NP',xCenter,yCenter, Block4);
[block_5_stimuli_db, Texture_WB] = block_distribution_creator(block_distribution_exp,block_condition_matrix,firstBlock,varsNeeded,part_dimension,IMG_Folder,MyScreen,'NP',xCenter,yCenter, Block5);


% [r,c] = size(block_1_stimuli_db);
% block_2_stimuli_db = block_1_stimuli_db;
% block_2_stimuli_db = block_2_stimuli_db(randperm(r),2:c);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% MERGE ALL FOUR STIMULUS DB CELL ARRAYS
% -------------------------------------------
% master_stim_db = cat(1,block_1p_stimuli_db,block_1_stimuli_db);

% write for loop that outputs 1000 or more different master_stim_db 
% (all code above this line must be in the for loop)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ITERATE THROUGH STIMULI DB, READ IN IMAGES, CREATE TEXTURES & RECTS
% -------------------------------------------
% if want to run one block at a time, comment out
% the entire section titled: MERGE ALL FOUR STIMULUS DB CELL ARRAYS
% and pass in individual block stimuli databases to the run_block function

%-------------------------------------------------------------------------%
% % % % % % % % % % % % Text for instructions % % % % % % % % % % % % % % %
% introductiory instructions
txt_continue = '<< Press any key to continue >>';
txt_ready = ' << PRESS ANY KEY WHEN YOU ARE READY TO BEGIN >> ';
txt_intro1 = 'Welcome to the experiment.\n This study consists of 5 blocks. You will be given a specific car\n to search for. You will search for this same car in all 5 blocks.';
txt_intro2 = 'Cars will flash briefly on the screen. When you see the\n target car, you will press the spacebar key. You will only respond\n if you see the target car.';
txt_intro3 = 'Before beginning the first block, you will practice searching\n for the right target car.';


txt_record = 'Experimenter Press Record on EEG';

txt_prac1 = 'You will now begin your practice block.\n You will practice searching for the car below for a few minutes.\n Remember to only respond when you see the car below.';
txt_first_block = 'Now that you are done practicing, we will start first the block.\n Remember to only respond when you see the car below.';
txt_start_block = 'We will now start the next block. \n Remember to only respond when you see the car below.';
txt_break = 'The block is over. You may take a short break if you wish.';

txt_outro = 'Congrats, you are all done!\n The experimenters will now come remove your cap.';
txt_close = ' '; 

%-------------------------------------------------------------------------%

% present introductory instructions below
instruct_text(txt_intro1, txt_continue, MyScreen, screenYpixels, DEBUG_CODE);
instruct_text(txt_intro2, txt_continue, MyScreen, screenYpixels, DEBUG_CODE);
instruct_text(txt_intro3, txt_continue, MyScreen, screenYpixels, DEBUG_CODE);
instruct_text(txt_record, txt_continue, MyScreen, screenYpixels, DEBUG_CODE);

% practice block 1
instruct_image(txt_prac1, txt_continue, MyScreen, screenYpixels, firstBlock, DEBUG_CODE, Texture_WB);
run_prac_block(dataFile,part_num,part_initials,cur_date,block_1p_stimuli_db,MyScreen,STIM_DUR,ISI,xCenter,yCenter,v_spacing,h_spacing, Texture_WB);

% experiment block 1
instruct_image(txt_first_block, txt_continue, MyScreen, screenYpixels, firstBlock, DEBUG_CODE, Texture_WB);
run_block(dataFile,part_num,part_initials,cur_date, block_1_stimuli_db,MyScreen,STIM_DUR,ISI, xCenter, yCenter,v_spacing,h_spacing, Texture_WB);
instruct_text(txt_break, txt_continue, MyScreen, screenYpixels, DEBUG_CODE);

% experiment block 2
instruct_image(txt_start_block, txt_continue, MyScreen, screenYpixels, firstBlock, DEBUG_CODE, Texture_WB);
run_block(dataFile,part_num,part_initials,cur_date,block_2_stimuli_db,MyScreen,STIM_DUR,ISI, xCenter, yCenter,v_spacing,h_spacing, Texture_WB);
instruct_text(txt_break, txt_continue, MyScreen, screenYpixels, DEBUG_CODE);

% experiment block 3
instruct_image(txt_start_block, txt_continue, MyScreen, screenYpixels, firstBlock, DEBUG_CODE, Texture_WB);
run_block(dataFile,part_num,part_initials,cur_date,block_3_stimuli_db,MyScreen,STIM_DUR,ISI, xCenter, yCenter,v_spacing,h_spacing, Texture_WB);
instruct_text(txt_break, txt_continue, MyScreen, screenYpixels, DEBUG_CODE);

% experiment block 4
instruct_image(txt_start_block, txt_continue, MyScreen, screenYpixels, firstBlock, DEBUG_CODE, Texture_WB);
run_block(dataFile,part_num,part_initials,cur_date,block_4_stimuli_db,MyScreen,STIM_DUR,ISI, xCenter, yCenter,v_spacing,h_spacing, Texture_WB);
instruct_text(txt_break, txt_continue, MyScreen, screenYpixels, DEBUG_CODE);

% experiment block 5
instruct_image(txt_start_block, txt_continue, MyScreen, screenYpixels, firstBlock, DEBUG_CODE, Texture_WB);
run_block(dataFile,part_num,part_initials,cur_date,block_5_stimuli_db,MyScreen,STIM_DUR,ISI, xCenter, yCenter,v_spacing,h_spacing, Texture_WB);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% PRINT CLOSING MESSAGE
% -------------------------------------------
instruct_text(txt_outro, txt_close, MyScreen, screenYpixels, DEBUG_CODE);

% close the screen


Screen('CloseAll');
sca;
end
end

% Doesn't send pp to comp
function run_prac_block(dataFile,part_num,part_initials,cur_date,master_stim_db,MyScreen,STIM_DUR,ISI,xCenter,yCenter,v_spacing,h_spacing, Texture_WB)
   % configure keyboard response key(s)
    KbName('UnifyKeyNames');
    space = KbName('space');
    %space = KbName('space');
    
    % get number of rows, not columns
    nrows_db = size(master_stim_db);
    nrows_db = nrows_db(1);
    
    % eeg code constants
    correct_response = 255;
    incorrect_response = 254;
    just_response = 253;
    
    % calculate post-stim interval
    POST_STIM_INT = ISI;
    
    % set parallel port address for EEG machine
    %pportaddress = uint16(53264);
    
    % set pin numbers
    pinnums = 9:-1:2;
    
    % create container for all logical values, to lookup EEG code
    mylogs = {};
    for i = 1:255
        mybin = dec2bin(i,numel(pinnums));
        mylog = logical(num2str(mybin)*1+'0'-96); %got this online somehow converts a dec to an array
        mylogs = [mylogs mylog];
    end

    for i = 1:nrows_db
        % get trial elements for file writing
        % replace all first digit 1s with 'i' [iteration element] from for loop
        BlockTarget = master_stim_db{i,1};
        CurTrial = master_stim_db{i,2};
        AbsolutePosition = master_stim_db{i,5};
        FileName = master_stim_db{i,6};
        SearchType = master_stim_db{i,7};
        RelevanceDimension = master_stim_db{i,8};
        StepsDimension = master_stim_db{i,9};
        EEG_Code = master_stim_db{i,10};
        Part_Axis = master_stim_db{i,11};
        %Texture = master_stim_db{i,12};
        isPractice = master_stim_db{i,13};
        %textureLoc = master_stim_db{i,15};
        Response_code = master_stim_db{i,16};
        BlockNum = master_stim_db{i,17};
        
        % Pull filename from !!!!master_stim_db!!! and compare it TEXTURE_WB; very
        % important to pull the name from there, because they will be
        % shuffled in there

        if strcmp(FileName, 'CMP300_1.bmp')
            cur_texture = Texture_WB{1, 2};
            textureLoc = Texture_WB{1, 4};
        elseif strcmp(FileName, 'CMP300_2.bmp')
            cur_texture = Texture_WB{2, 2};
            textureLoc = Texture_WB{2, 4};
        elseif strcmp(FileName, 'CMP300_3.bmp')
            cur_texture = Texture_WB{3, 2};
            textureLoc = Texture_WB{3, 4};
        elseif strcmp(FileName, 'CMP300_4.bmp')
            cur_texture = Texture_WB{4, 2};
            textureLoc = Texture_WB{4, 4};
        elseif strcmp(FileName, 'CMP300_6.bmp')
            cur_texture = Texture_WB{5, 2};
            textureLoc = Texture_WB{5, 4};
        elseif strcmp(FileName, 'CMP300_7.bmp')
            cur_texture = Texture_WB{6, 2};
            textureLoc = Texture_WB{6, 4};
        elseif strcmp(FileName, 'CMP300_8.bmp')
            cur_texture = Texture_WB{7, 2};
            textureLoc = Texture_WB{7, 4};
        elseif strcmp(FileName, 'CMP300_9.bmp')
            cur_texture = Texture_WB{8, 2};
            textureLoc = Texture_WB{8, 4};
        end

        Texture = cur_texture;
        
        % Inter-stimulus screen
        DrawFormattedText(MyScreen, '+', [(xCenter + v_spacing)], [(yCenter + h_spacing)], [255, 255, 255], [], [], [], [2]);
        Screen('Flip', MyScreen);
        WaitSecs(ISI/2);
        
        % Draw stimulus
        Screen('DrawTexture', MyScreen, Texture, [], textureLoc); % Draw the image to the screen;
        [~,startrt] = Screen('Flip', MyScreen); % present to the screen
        %pp(uint8(pinnums),mylogs{EEG_Code},false,uint8(0),pportaddress); % write to some pins (fast -- dangerous if addr is incorrect)
        %pp(uint8(pinnums),[0 0 0 0 0 0 0 0],false,uint8(0),pportaddress); % write to some pins (fast -- dangerous if addr is incorrect)
        
        % set initial presentation counter
        presscounter = 0;
        curr_time = datestr(now, 'HH:MM:SS'); % string formatted timestamp
        user_response = '0';
        Accuracy = 2;
        RT = 9.999;
        
        while (GetSecs-startrt <= STIM_DUR)
            [KeyIsDown, endrt, KeyCode]=KbCheck; % check the KB
            if KeyIsDown
                response_only_EEG_code = mylogs{just_response};
                
                % send EEG codes
                %pp(uint8(pinnums),response_only_EEG_code,false,uint8(0),pportaddress); % write to some pins (fast -- dangerous if addr is incorrect)
                %pp(uint8(pinnums),[0 0 0 0 0 0 0 0],false,uint8(0),pportaddress); % write to some pins (fast -- dangerous if addr is incorrect)
               
                %events = [events; {GetSecs-expStart KbName(KeyCode)}];
                
                % calculate RT, get response, timestamp
                RT = endrt-startrt; % returned by GetSecs
                curr_time = datestr(now, 'HH:MM:SS'); % string formatted timestamp
                response = KbName(KeyCode);
                
                % check for response
                if iscell(response)
                    user_response = '0';
                else
                    user_response = '1';
                end                

                corr_response = strcmp(Response_code,user_response);
                %disp(corr_response);

                % determine accuracy and send a code for correct/incorrect, 
                % for easy rejection of incorrect trials
                if corr_response
                    correct = correct_response; % EEG Code
                    Accuracy = 1;
                else
                    correct = incorrect_response; % EEG Code
                    Accuracy = 0;
                end

                % send response code to EEG machine
                accuracy_code = correct;
                accuracy_EEG_code = mylogs{accuracy_code};
                %pp(uint8(pinnums),accuracy_EEG_code,false,uint8(0),pportaddress); % write to some pins (fast -- dangerous if addr is incorrect)
                %pp(uint8(pinnums),[0 0 0 0 0 0 0 0],false,uint8(0),pportaddress); % write to some pins (fast -- dangerous if addr is incorrect)

                presscounter = 1;
                break
            end % END -- when is pressed
        end % END -- Initial while keycheck
        
        
        % wait the rest of the time if necessary; only necessary if presscounter == 1
        while (GetSecs-startrt <= STIM_DUR) 
        end
            
        % Turn off the stimulus; keep listening after stimulus goes away; listen until the next trial
        % while loop should just be set to listen during stim-duration; not kbcheck 
        % Use press counter
        
%         Screen('DrawTexture', MyScreen, Texture, [], textureLoc);
        
        % Inter-stimulus screen
        DrawFormattedText(MyScreen, '+', [(xCenter + v_spacing)], [(yCenter + h_spacing)], [255, 255, 255], [], [], [], [2]);
        Screen('Flip', MyScreen); % BLANK SCREEN
        
        %?%!% NEWLY ADDED %?%!%
        % If response during stimulus, still waits ISI instead of skipping
        if presscounter == 1;
            WaitSecs(ISI);
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        if ~presscounter
            while (GetSecs-startrt <= POST_STIM_INT)
                [KeyIsDown, endrt, KeyCode]=KbCheck;
                if KeyIsDown
                    response_only_EEG_code = mylogs{just_response};
                    
                    % send EEG codes
                    %pp(uint8(pinnums),response_only_EEG_code,false,uint8(0),pportaddress); % write to some pins (fast -- dangerous if addr is incorrect)
                    %pp(uint8(pinnums),[0 0 0 0 0 0 0 0],false,uint8(0),pportaddress); % write to some pins (fast -- dangerous if addr is incorrect)
                   
                    %events = [events; {GetSecs-expStart KbName(KeyCode)}];
                    
                    % calculate RT, get response, timestamp
                    RT = endrt-startrt;
                    curr_time = datestr(now, 'HH:MM:SS'); % string formatted timestamp
                    response = KbName(KeyCode);
                    
                    % check for response
                    if iscell(response)
                        user_response = '0';
                    else
                        user_response = '1';
                    end                

                    % compare value in stim db to user response to
                    % determine if correct
                    corr_response = strcmp(Response_code,user_response);
                    %disp(corr_response);

                    % determine accuracy and send a code for correct/incorrect, 
                    % for easy rejection of incorrect trials
                    if corr_response
                        correct = correct_response; % EEG Code
                        Accuracy = 1;
                    else
                        correct = incorrect_response; % EEG Code
                        Accuracy = 0;
                    end
                   
                    accuracy_code = correct;
                    accuracy_EEG_code = mylogs{accuracy_code};
                    %pp(uint8(pinnums),accuracy_EEG_code,false,uint8(0),pportaddress); % write to some pins (fast -- dangerous if addr is incorrect)
                    %pp(uint8(pinnums),[0 0 0 0 0 0 0 0],false,uint8(0),pportaddress); % write to some pins (fast -- dangerous if addr is incorrect)
                    
                    presscounter = 2; %CHANGED THIS TO 2 FOR THE LOOP BELOW
                    
                    break
                else
                    % compare value in stim db to user response to
                    % determine if correct
                    corr_response = strcmp(Response_code,user_response);
                    %disp(corr_response);

                    % figure out if it is correct and send a code for
                    % correct/incorrect so we can reject incorrect trials
                    % easily
                    % determine accuracy
                    if corr_response
                        Accuracy = 1;
                    else
                        Accuracy = 0;
                    end
                end
            end
        end
        
        
        %%% NEED TO HAVE A LOOP WHICH WAITS THE LEFTOVER TIME IF KB
        %%% RESPONSE HAPPENS DURING ISI. THE KB RESPONSE TERMINATES THE
        %%% LOOP EARLY 
        LeftoverTime = ISI - RT;
        disp(LeftoverTime);
        
        if presscounter == 2
            WaitSecs(LeftoverTime)
        end
        
        % >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        % FILE WRITTING, TRIAL DATA
        % >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
        % open file for writing
        inputFile = fopen(dataFile, 'a'); %Opens the file I want to record my text to

        % write all vars to file
        fprintf(inputFile, '%s\t', part_num); % participant number
        fprintf(inputFile, '%s\t', part_initials); % participant initials
        fprintf(inputFile, '%s\t', cur_date); % run date
        fprintf(inputFile, '%s\t', curr_time); % run time
        fprintf(inputFile, '%s\t', BlockTarget); % Block target
        fprintf(inputFile, '%d\t', BlockNum); % Block Number
        fprintf(inputFile, '%d\t', CurTrial); % Trial Number
        fprintf(inputFile, '%s\t', isPractice); % Trial Number
        fprintf(inputFile, '%s\t', AbsolutePosition); % absolute position morph space
        fprintf(inputFile, '%s\t', FileName); % filename
        fprintf(inputFile, '%s\t', SearchType); % search type, targ/nontarg
        fprintf(inputFile, '%s\t', RelevanceDimension); % relevant, irrelevant, RI, IR
        fprintf(inputFile, '%s\t', StepsDimension); % 1, 2, 2-1
        fprintf(inputFile, '%d\t', EEG_Code); % 1-56
        fprintf(inputFile, '%s\t', Part_Axis); % Horizontal/Vertical
        fprintf(inputFile, '%f\t', RT); % RT recoded to take into account timeout trials
        fprintf(inputFile, '%d\t', Accuracy); % RT recoded to take into account timeout trials
        fprintf(inputFile, '\n'); % blank space
        
        % close file until next trial
        fclose(inputFile);
    end % end of looping through stimulus db
end % end of function


function run_block(dataFile,part_num,part_initials,cur_date,master_stim_db,MyScreen,STIM_DUR,ISI, xCenter, yCenter,v_spacing,h_spacing, Texture_WB)
    % configure keyboard response key(s)
    KbName('UnifyKeyNames');
    space = KbName('space');
    %space = KbName('space');
    
    % get number of rows, not columns
    nrows_db = size(master_stim_db);
    nrows_db = nrows_db(1);
    
    % eeg code constants
    correct_response = 255;
    incorrect_response = 254;
    just_response = 253;
    
    % calculate post-stim interval
    POST_STIM_INT = ISI;
    
    % set parallel port address for EEG machine
    %pportaddress = uint16(53264);
    
    % set pin numbers
    pinnums = 9:-1:2;
    
    % create container for all logical values, to lookup EEG code
    mylogs = {};
    for i = 1:255
        mybin = dec2bin(i,numel(pinnums));
        mylog = logical(num2str(mybin)*1+'0'-96); %got this online somehow converts a dec to an array
        mylogs = [mylogs mylog];
    end

    for i = 1:nrows_db
        % get trial elements for file writing
        % replace all first digit 1s with 'i' [iteration element] from for loop
        BlockTarget = master_stim_db{i,1};
        CurTrial = master_stim_db{i,2};
        AbsolutePosition = master_stim_db{i,5};
        FileName = master_stim_db{i,6};
        SearchType = master_stim_db{i,7};
        RelevanceDimension = master_stim_db{i,8};
        StepsDimension = master_stim_db{i,9};
        EEG_Code = master_stim_db{i,10};
        Part_Axis = master_stim_db{i,11};
        %Texture = master_stim_db{i,12};
        isPractice = master_stim_db{i,13};
        %textureLoc = master_stim_db{i,15};
        Response_code = master_stim_db{i,16};
        BlockNum = master_stim_db{i, 17};
        
        % Pull filename from !!!!master_stim_db!!! and compare it TEXTURE_WB; very
        % important to pull the name from there, because they will be
        % shuffled in there

        if strcmp(FileName, 'CMP300_1.bmp')
            cur_texture = Texture_WB{1, 2};
            textureLoc = Texture_WB{1, 4};
        elseif strcmp(FileName, 'CMP300_2.bmp')
            cur_texture = Texture_WB{2, 2};
            textureLoc = Texture_WB{2, 4};
        elseif strcmp(FileName, 'CMP300_3.bmp')
            cur_texture = Texture_WB{3, 2};
            textureLoc = Texture_WB{3, 4};
        elseif strcmp(FileName, 'CMP300_4.bmp')
            cur_texture = Texture_WB{4, 2};
            textureLoc = Texture_WB{4, 4};
        elseif strcmp(FileName, 'CMP300_6.bmp')
            cur_texture = Texture_WB{5, 2};
            textureLoc = Texture_WB{5, 4};
        elseif strcmp(FileName, 'CMP300_7.bmp')
            cur_texture = Texture_WB{6, 2};
            textureLoc = Texture_WB{6, 4};
        elseif strcmp(FileName, 'CMP300_8.bmp')
            cur_texture = Texture_WB{7, 2};
            textureLoc = Texture_WB{7, 4};
        elseif strcmp(FileName, 'CMP300_9.bmp')
            cur_texture = Texture_WB{8, 2};
            textureLoc = Texture_WB{8, 4};
        end

        Texture = cur_texture;

        % Inter-stimulus screen
        DrawFormattedText(MyScreen, '+', [(xCenter + v_spacing)], [(yCenter + h_spacing)], [255, 255, 255], [], [], [], [2]);
        Screen('Flip', MyScreen);
        WaitSecs(ISI/2);
        
        % Draw stimulus
        Screen('DrawTexture', MyScreen, Texture, [], textureLoc); % Draw the image to the screen;
        [~,startrt] = Screen('Flip', MyScreen); % present to the screen
        %pp(uint8(pinnums),mylogs{EEG_Code},false,uint8(0),pportaddress); % write to some pins (fast -- dangerous if addr is incorrect)
        %pp(uint8(pinnums),[0 0 0 0 0 0 0 0],false,uint8(0),pportaddress); % write to some pins (fast -- dangerous if addr is incorrect)
        
        % set initial presentation counter
        presscounter = 0;
        curr_time = datestr(now, 'HH:MM:SS'); % string formatted timestamp
        user_response = '0';
        Accuracy = 2;
        RT = 9.999;
        
        while (GetSecs-startrt <= STIM_DUR)
            [KeyIsDown, endrt, KeyCode]=KbCheck; % check the KB
            if KeyIsDown
                response_only_EEG_code = mylogs{just_response};
                
                % send EEG codes
                %pp(uint8(pinnums),response_only_EEG_code,false,uint8(0),pportaddress); % write to some pins (fast -- dangerous if addr is incorrect)
                %pp(uint8(pinnums),[0 0 0 0 0 0 0 0],false,uint8(0),pportaddress); % write to some pins (fast -- dangerous if addr is incorrect)
               
                %events = [events; {GetSecs-expStart KbName(KeyCode)}];
                
                % calculate RT, get response, timestamp
                RT = endrt-startrt; % returned by GetSecs
                curr_time = datestr(now, 'HH:MM:SS'); % string formatted timestamp
                response = KbName(KeyCode);
                
                % check for response
                if iscell(response)
                    user_response = '0';
                else
                    user_response = '1';
                end                

                corr_response = strcmp(Response_code,user_response);
                %disp(corr_response);

                % determine accuracy and send a code for correct/incorrect, 
                % for easy rejection of incorrect trials
                if corr_response
                    correct = correct_response; % EEG Code
                    Accuracy = 1;
                else
                    correct = incorrect_response; % EEG Code
                    Accuracy = 0;
                end

                % send response code to EEG machine
                accuracy_code = correct;
                accuracy_EEG_code = mylogs{accuracy_code};
                %pp(uint8(pinnums),accuracy_EEG_code,false,uint8(0),pportaddress); % write to some pins (fast -- dangerous if addr is incorrect)
                %pp(uint8(pinnums),[0 0 0 0 0 0 0 0],false,uint8(0),pportaddress); % write to some pins (fast -- dangerous if addr is incorrect)

                presscounter = 1;
                break
            end % END -- when is pressed
        end % END -- Initial while keycheck
        
        
        % wait the rest of the time if necessary; only necessary if presscounter == 1
        while (GetSecs-startrt <= STIM_DUR) 
        end
            
        % Turn off the stimulus; keep listening after stimulus goes away; listen until the next trial
        % while loop should just be set to listen during stim-duration; not kbcheck 
        % Use press counter
        
%         Screen('DrawTexture', MyScreen, Texture, [], textureLoc);
        
        % Inter-stimulus screen
        DrawFormattedText(MyScreen, '+', [(xCenter + v_spacing)], [(yCenter + h_spacing)], [255, 255, 255], [], [], [], [2]);
        Screen('Flip', MyScreen); % BLANK SCREEN
        
        %?%!% NEWLY ADDED %?%!%
        % If response during stimulus, still waits ISI instead of skipping
        if presscounter == 1;
            WaitSecs(ISI);
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        if ~presscounter
            while (GetSecs-startrt <= POST_STIM_INT)
                [KeyIsDown, endrt, KeyCode]=KbCheck;
                if KeyIsDown
                    response_only_EEG_code = mylogs{just_response};
                    
                    % send EEG codes
                    %pp(uint8(pinnums),response_only_EEG_code,false,uint8(0),pportaddress); % write to some pins (fast -- dangerous if addr is incorrect)
                    %pp(uint8(pinnums),[0 0 0 0 0 0 0 0],false,uint8(0),pportaddress); % write to some pins (fast -- dangerous if addr is incorrect)
                   
                    %events = [events; {GetSecs-expStart KbName(KeyCode)}];
                    
                    % calculate RT, get response, timestamp
                    RT = endrt-startrt;
                    curr_time = datestr(now, 'HH:MM:SS'); % string formatted timestamp
                    response = KbName(KeyCode);
                    
                    % check for response
                    if iscell(response)
                        user_response = '0';
                    else
                        user_response = '1';
                    end                

                    % compare value in stim db to user response to
                    % determine if correct
                    corr_response = strcmp(Response_code,user_response);
                    %disp(corr_response);

                    % determine accuracy and send a code for correct/incorrect, 
                    % for easy rejection of incorrect trials
                    if corr_response
                        correct = correct_response; % EEG Code
                        Accuracy = 1;
                    else
                        correct = incorrect_response; % EEG Code
                        Accuracy = 0;
                    end
                   
                    accuracy_code = correct;
                    accuracy_EEG_code = mylogs{accuracy_code};
                    %pp(uint8(pinnums),accuracy_EEG_code,false,uint8(0),pportaddress); % write to some pins (fast -- dangerous if addr is incorrect)
                    %pp(uint8(pinnums),[0 0 0 0 0 0 0 0],false,uint8(0),pportaddress); % write to some pins (fast -- dangerous if addr is incorrect)
                    
                    presscounter = 2; %CHANGED THIS TO 2 FOR THE LOOP BELOW
                    
                    break
                else
                    % compare value in stim db to user response to
                    % determine if correct
                    corr_response = strcmp(Response_code,user_response);
                    %disp(corr_response);

                    % figure out if it is correct and send a code for
                    % correct/incorrect so we can reject incorrect trials
                    % easily
                    % determine accuracy
                    if corr_response
                        Accuracy = 1;
                    else
                        Accuracy = 0;
                    end
                end
            end
        end
        
        
        %%% NEED TO HAVE A LOOP WHICH WAITS THE LEFTOVER TIME IF KB
        %%% RESPONSE HAPPENS DURING ISI. THE KB RESPONSE TERMINATES THE
        %%% LOOP EARLY 
        LeftoverTime = ISI - RT;
        disp(LeftoverTime);
        
        if presscounter == 2
            WaitSecs(LeftoverTime)
        end
        
        % >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        % FILE WRITTING, TRIAL DATA
        % >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
        % open file for writing
        inputFile = fopen(dataFile, 'a'); %Opens the file I want to record my text to

        % write all vars to file
        fprintf(inputFile, '%s\t', part_num); % participant number
        fprintf(inputFile, '%s\t', part_initials); % participant initials
        fprintf(inputFile, '%s\t', cur_date); % run date
        fprintf(inputFile, '%s\t', curr_time); % run time
        fprintf(inputFile, '%s\t', BlockTarget); % Block target
        fprintf(inputFile, '%d\t', BlockNum); % Block Number
        fprintf(inputFile, '%d\t', CurTrial); % Trial Number
        fprintf(inputFile, '%s\t', isPractice); % Trial Number
        fprintf(inputFile, '%s\t', AbsolutePosition); % absolute position morph space
        fprintf(inputFile, '%s\t', FileName); % filename
        fprintf(inputFile, '%s\t', SearchType); % search type, targ/nontarg
        fprintf(inputFile, '%s\t', RelevanceDimension); % relevant, irrelevant, RI, IR
        fprintf(inputFile, '%s\t', StepsDimension); % 1, 2, 2-1
        fprintf(inputFile, '%d\t', EEG_Code); % 1-56
        fprintf(inputFile, '%s\t', Part_Axis); % Horizontal/Vertical
        fprintf(inputFile, '%f\t', RT); % RT recoded to take into account timeout trials
        fprintf(inputFile, '%d\t', Accuracy); % RT recoded to take into account timeout trials
        fprintf(inputFile, '\n'); % blank space
        
        % close file until next trial
        fclose(inputFile);
    end % end of looping through stimulus db
end % end of function


function [stimuli_db, Texture_WB] = block_distribution_creator(block_distribution,block_condition_matrix,block_target,varsNeeded,part_dimension,IMG_Folder,MyScreen,practiceVar,xCenter,yCenter, BlockNum)
    % copy distribution from master list, and shuffle it
    block_distribution_copy = block_distribution;
    block_distribution_copy = Shuffle(block_distribution_copy);
    
    % find the row number, where first column's value
    % matches the value for the first block
    current_row = block_condition_matrix(:,1)==num2str(block_target);
    
    % store that row's data
    current_block = block_condition_matrix(current_row,:);

    % create cell array to store stimuli information
    stimuli_db = cell(length(block_distribution_copy),varsNeeded);

    % for block 1
    % loop through distribution to present each trial
    for i=1:length(block_distribution_copy)
        % get element from weighted distribution
        elm = block_distribution_copy(i);

        % lookup current image based on selected
        % item from the distribution sampled
        absolute_pos = current_block(elm);

        % current element minus 1 = condition code for eeg
        condition_num = num2str(elm - 1);

        % determine stimulis dimension
        % T = Target
        % R =  Relevant
        % I = Irrelevant
        % RI = Relevant, Irrelevant
        % IR = Irrelevant, Relevant
        % RRII = 2 steps, Relevant & irrelevant
        if absolute_pos == block_target
            searchType = 'Target';
            relevanceDim = 'T';
            stepsDim = '0';
        else
            if elm == 2
                relevanceDim = 'R';
                stepsDim = '1';
            elseif elm == 3
                relevanceDim = 'R';
                stepsDim = '2';
            elseif elm == 4
                relevanceDim = 'I';
                stepsDim = '1';
            elseif elm == 5
                relevanceDim = 'I';
                stepsDim = '2';
            elseif elm == 6
                relevanceDim = 'RI';
                stepsDim = '21';
            elseif elm == 7
                relevanceDim = 'IR';
                stepsDim = '21';
            elseif elm == 8
                relevanceDim = 'RRII';
                stepsDim = '22';
            end
            searchType = 'Non-Target';
        end

        % generate EEG code
        reset_code = 0; % to turn pin off
        start_code = reset_code + 1; % beginning of matrix (see Excel)

        % first determine if target or nontarget
        if relevanceDim == 'T'
            EEG_code = start_code;
            Response_code = '1';
        else
            addition = 8;
            EEG_code = start_code + addition;
            Response_code = '0';
        end

        % add +4 for vertical | +0 for horizontal
        if part_dimension == 'V'
            addition = 0;
            EEG_code = EEG_code + addition;
        elseif part_dimension == 'H'
            addition = 4;
            EEG_code = EEG_code + addition;
        end

        % add +1 for each row down from target = 1
        if block_target == '1'
            EEG_code = EEG_code + 0;
        elseif block_target == '3'
            EEG_code = EEG_code + 1;
        elseif block_target == '7'
            EEG_code = EEG_code + 2;
        elseif block_target == '9'
            EEG_code = EEG_code + 3;
        end

        % add +8 for each level of relevance, +0 for target
        if strcmp(relevanceDim,'R') && strcmp(stepsDim,'1')
            EEG_code = EEG_code + 0;
        elseif strcmp(relevanceDim,'R') && strcmp(stepsDim,'2')
            EEG_code = EEG_code + (8 * 1);
        elseif strcmp(relevanceDim,'I') && strcmp(stepsDim,'1')
            EEG_code = EEG_code + (8 * 2);
        elseif strcmp(relevanceDim,'I') && strcmp(stepsDim,'2')
            EEG_code = EEG_code + (8 * 3);
        elseif strcmp(relevanceDim,'RI') && strcmp(stepsDim,'21')
            EEG_code = EEG_code + (8 * 4);
        elseif strcmp(relevanceDim,'IR') && strcmp(stepsDim,'21')
            EEG_code = EEG_code + (8 * 5);
        elseif strcmp(relevanceDim,'RRII') && strcmp(stepsDim,'22')
            EEG_code = EEG_code + (8 * 6);
        end

        % concatenate and print filename
        filename = strcat('CMP300_',num2str(absolute_pos));
        filename = strcat(filename,'.bmp');
        
        % if debugging, turn on filename printing
        % disp(filename); 

        % add data to trial list stimulus database
        % columns of stim db listed below in order
        % block | trial  | image | searchType | relevance | distance
        stimuli_db{i,1} = block_target;
        stimuli_db{i,2} = i;
        stimuli_db{i,3} = elm;
        stimuli_db{i,4} = condition_num;
        stimuli_db{i,5} = absolute_pos;
        stimuli_db{i,6} = filename;
        stimuli_db{i,7} = searchType;
        stimuli_db{i,8} = relevanceDim;
        stimuli_db{i,9} = stepsDim;
        stimuli_db{i,10} = EEG_code;
        stimuli_db{i,11} = part_dimension;
        %stimuli_db{i,12} = cur_texture;
        stimuli_db{i,13} = practiceVar;
        %stimuli_db{i,14} = sourceRect;
        %stimuli_db{i,15} = textureLoc;
        stimuli_db{i,16} = Response_code;
        stimuli_db{i,17} = BlockNum;
    end
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Create Texture_WB
    Num_of_Textures = 8; % 8 pics, therefore 8 textures
    Num_of_Textures_Columns = 4; % 4 columns containing (filename, texture, sourceRect, textureLoc)
    Texture_WB = cell(Num_of_Textures, Num_of_Textures_Columns);
    
    % Variable containing all the FileNames of pics
    CAR_PICS = {'CMP300_1.bmp' 'CMP300_2.bmp' 'CMP300_3.bmp' 'CMP300_4.bmp'...
        'CMP300_6.bmp' 'CMP300_7.bmp' 'CMP300_8.bmp' 'CMP300_9.bmp'};
    
    for i = 1:Num_of_Textures
        
        filename = char(CAR_PICS(i));
        
        % pre-load image---------------------------------------------------
        img_preloaded = imread([IMG_Folder filename]);    
        %resize image
        img_loaded = imresize(img_preloaded, .45);
        % create texture from image
        TEXTURE = Screen('MakeTexture', MyScreen, img_loaded); 
        % texture -> rect
        sourceRect = Screen('Rect', TEXTURE); %Make Texture into rect
        % relocate rect
        textureLoc = CenterRectOnPoint(sourceRect, xCenter, yCenter);
        %------------------------------------------------------------------
        
        Texture_WB{i, 1} = filename;
        Texture_WB{i, 2} = TEXTURE;
        Texture_WB{i, 3} = sourceRect;
        Texture_WB{i, 4} = textureLoc;
        
    end
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % ADD TEXTURE_WB VARIABLE TO RUNBLOCK FUNCTIONS
    % MOVE IF STATEMENT TO RUNBLOCK FUNCTIONS
    
    % if statement linking FileName to Texture (Might need to do this in
    % the RUN_BLOCK function
        
    % Pull filename from !!!!STIM_WB!!! and compare it TEXTURE_WB; very
    % important to pull the name from STIM_WB, because they will be
    % shuffled in there
    
    if strcmp(filename, 'CMP300_1.bmp')
        cur_texture = Texture_WB{1, 2};
        sourceRect = Texture_WB{1, 3};
        textureLoc = Texture_WB{1, 4};
    elseif strcmp(filename, 'CMP300_2.bmp')
        cur_texture = Texture_WB{2, 2};
        sourceRect = Texture_WB{2, 3};
        textureLoc = Texture_WB{2, 4};
    elseif strcmp(filename, 'CMP300_3.bmp')
        cur_texture = Texture_WB{3, 2};
        sourceRect = Texture_WB{3, 3};
        textureLoc = Texture_WB{3, 4};
    elseif strcmp(filename, 'CMP300_4.bmp')
        cur_texture = Texture_WB{4, 2};
        sourceRect = Texture_WB{4, 3};
        textureLoc = Texture_WB{4, 4};
    elseif strcmp(filename, 'CMP300_6.bmp')
        cur_texture = Texture_WB{5, 2};
        sourceRect = Texture_WB{5, 3};
        textureLoc = Texture_WB{5, 4};
    elseif strcmp(filename, 'CMP300_7.bmp')
        cur_texture = Texture_WB{6, 2};
        sourceRect = Texture_WB{6, 3};
        textureLoc = Texture_WB{6, 4};
    elseif strcmp(filename, 'CMP300_8.bmp')
        cur_texture = Texture_WB{7, 2};
        sourceRect = Texture_WB{7, 3};
        textureLoc = Texture_WB{7, 4};
    elseif strcmp(filename, 'CMP300_9.bmp')
        cur_texture = Texture_WB{8, 2};
        sourceRect = Texture_WB{8, 3};
        textureLoc = Texture_WB{8, 4};
    end
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    
    
end

function instruct_image(text_prac, txt_continue, MyScreen, screenYpixels, target_iden, DEBUG_CODE, Texture_WB)
    % concatenate filename
    filename = strcat('CMP300_',num2str(target_iden));
    filename = strcat(filename,'.bmp');
    
    if strcmp(filename, 'CMP300_1.bmp')
        cur_texture = Texture_WB{1, 2};
        sourceRect = Texture_WB{1, 3};
        textureLoc = Texture_WB{1, 4};
    elseif strcmp(filename, 'CMP300_2.bmp')
        cur_texture = Texture_WB{2, 2};
        sourceRect = Texture_WB{2, 3};
        textureLoc = Texture_WB{2, 4};
    elseif strcmp(filename, 'CMP300_3.bmp')
        cur_texture = Texture_WB{3, 2};
        sourceRect = Texture_WB{3, 3};
        textureLoc = Texture_WB{3, 4};
    elseif strcmp(filename, 'CMP300_4.bmp')
        cur_texture = Texture_WB{4, 2};
        sourceRect = Texture_WB{4, 3};
        textureLoc = Texture_WB{4, 4};
    elseif strcmp(filename, 'CMP300_6.bmp')
        cur_texture = Texture_WB{5, 2};
        sourceRect = Texture_WB{5, 3};
        textureLoc = Texture_WB{5, 4};
    elseif strcmp(filename, 'CMP300_7.bmp')
        cur_texture = Texture_WB{6, 2};
        sourceRect = Texture_WB{6, 3};
        textureLoc = Texture_WB{6, 4};
    elseif strcmp(filename, 'CMP300_8.bmp')
        cur_texture = Texture_WB{7, 2};
        sourceRect = Texture_WB{7, 3};
        textureLoc = Texture_WB{7, 4};
    elseif strcmp(filename, 'CMP300_9.bmp')
        cur_texture = Texture_WB{8, 2};
        sourceRect = Texture_WB{8, 3};
        textureLoc = Texture_WB{8, 4};
    end

    % text positions
    yTop = screenYpixels*.15;
    yBottom = screenYpixels*.85;

    % sample text
    DrawFormattedText(MyScreen, text_prac, 'center', yTop, [255, 255, 255], [], [], [], [2]);
    DrawFormattedText(MyScreen, txt_continue, 'center', yBottom, [255, 255, 255], [], [], [], [2]);  
    Screen('DrawTexture', MyScreen, cur_texture, [], textureLoc);
    
    % show stimulus
    Screen('Flip', MyScreen);
    
    if DEBUG_CODE == 0
        KbStrokeWait; 
        WaitSecs(0.2);
    else
        WaitSecs(.01)
    end
    
end

function instruct_text(text_intro, txt_continue, MyScreen, screenYpixels, DEBUG_CODE)

    yBottom = screenYpixels*.85;

    % sample text
    DrawFormattedText(MyScreen, text_intro, 'center', 'center', [255, 255, 255], [], [], [], [2]);
    DrawFormattedText(MyScreen, txt_continue, 'center', yBottom, [255, 255, 255], [], [], [], [2]);
    Screen('Flip', MyScreen);
    
    if DEBUG_CODE== 0
        KbStrokeWait;
        WaitSecs(0.2);
    else
        WaitSecs(.01)
    end
    
end