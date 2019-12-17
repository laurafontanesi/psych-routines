from __future__ import division
from psychopy.visual import ImageStim, TextStim, Window
from psychopy import core, event, gui, data, logging
import numpy as np
import pandas as pd
import os

from routines import Routine

# Code for the (simplified) reinforcement learning task from Fontanesi and colleagues (https://doi.org/10.3758/s13423-018-1554-2)

#general settings
expName = 'example_4'
screen_size = [800, 600]
frames_per_second = 60
full_screen = False
background_color = '#eeeeee'

# trial settings
choice_keys = ['q', 'p']
escape_key = 'escape'
choice_time_limit = 3
feedback_duration = 2
fixation_duration = 1

#stimuli settings
text_color = 'black'
text_height = 50
options_x_offset = 200
image_size = 100

#store info about the experiment session
dlg = gui.Dlg(title=expName)
dlg.addField('Participant:', 1)
dlg.addField('Age:', 25)
dlg.addField('Gender:', choices=['female', 'male', 'prefer not to disclose'])
dlg.addField('Handedness:', choices=['right', 'left', 'both'])
dlg.show()

expInfo = dict(zip(['participant', 'age', 'gender', 'hand'], dlg.data))
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName # add the experiment name
if dlg.OK:  # then the user pressed OK
    print(expInfo)
else:
    print(expInfo)
    core.quit()

#check if data folder exists
directory=os.path.join(os.getcwd(), 'data')
if not os.path.exists(directory):
    os.makedirs(directory)

#create file name for storing data
fileName = os.path.join('data', '%s_%s_%s' % (expName, expInfo['participant'], expInfo['date']))

#save a log file
logFile = logging.LogFile(fileName + '.log', level=logging.DEBUG)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

#create a window
mywin = Window(screen_size, units='pix', color=background_color, fullscr=full_screen)

#create some stimuli
left_feedback = TextStim(win=mywin, color=text_color, pos=(-options_x_offset, 0), height=text_height)
right_feedback = TextStim(win=mywin, color=text_color, pos=(options_x_offset, 0), height=text_height)

left_picture = ImageStim(win=mywin, pos=(-options_x_offset, 0), size=image_size)
right_picture = ImageStim(win=mywin, pos=(options_x_offset, 0), size=image_size)

fixation_cross = TextStim(win=mywin, text='+', color=text_color)

n_trials = 20

rewards_A = np.random.normal(36, 5, 10).astype(int)
rewards_B = np.random.normal(40, 5, 10).astype(int)
rewards_C = np.random.normal(50, 5, 10).astype(int)
rewards_D = np.random.normal(54, 5, 10).astype(int)

stimuli = pd.DataFrame(
    {'trial_type': np.repeat(['AB', 'AC', 'BD', 'CD'], 5),
     'left_image': np.repeat(['A.png', 'D.png'], 10),
     'right_image': np.tile(np.repeat(['B.png', 'C.png'], 5), 2),
     'left_feedback': np.append(rewards_A, rewards_D),
     'right_feedback': 0
    })

stimuli.loc[stimuli.right_image == 'B.png', 'right_feedback'] = rewards_B
stimuli.loc[stimuli.right_image == 'C.png', 'right_feedback'] = rewards_C

stimuli = stimuli.sample(frac=1).reset_index(drop=True)
stimuli['trial'] = np.arange(n_trials)+1

#create the dataframe
data = pd.DataFrame([])

#draw the stimuli
trial_routine = Routine(window=mywin, frames_per_second=frames_per_second, escape_key=escape_key)

for t in range(n_trials):
    # put here things that change every trial
    left_feedback.text = '%s' % stimuli.loc[t, 'left_feedback']
    right_feedback.text = '%s' % stimuli.loc[t, 'right_feedback']
    
    left_picture.image = os.path.join(os.getcwd(), 'stimuli', 'example_4', stimuli.loc[t, 'left_image'])
    right_picture.image = os.path.join(os.getcwd(), 'stimuli', 'example_4', stimuli.loc[t, 'right_image'])

    # first event
    trial_routine.wait_for_time_limit(
        components=[fixation_cross], 
        time_seconds=fixation_duration, 
        label='fixation_cross')

    # second event
    key, rt = trial_routine.wait_for_keys_or_time_limit(
        components=[left_picture, right_picture], 
        valid_keys=choice_keys, 
        time_seconds=choice_time_limit, 
        label='gamble_choice')
    data = data.append({'rt':rt, 'choice': key, 'trial': t, 'f_right': stimuli.loc[t, 'right_feedback'],  'f_left': stimuli.loc[t, 'left_feedback'],
                        'i_right': stimuli.loc[t, 'right_image'],  'i_left': stimuli.loc[t, 'left_image'], 'trial_type': stimuli.loc[t, 'trial_type'],
                       }, ignore_index=True) # record the responses
    
    # third event
    trial_routine.wait_for_time_limit(
        components=[left_feedback, right_feedback], 
        time_seconds=feedback_duration, 
        label='feedback')

    #save data to file
    for label in expInfo.keys():
        data[label] = expInfo[label]
    data.to_csv(fileName + '.csv')
    
#cleanup
mywin.close()
core.quit()