from __future__ import division
from psychopy.visual import TextStim, Window
from psychopy import core, event, gui, data, logging
import numpy as np
import pandas as pd
import os

from routines import Routine

#general settings
expName = 'template'
screen_size = [800, 600]
frames_per_second = 60
full_screen = False
background_color = '#bfbfbf'

# trial settings
response_deadline = 5
choice_keys = ['q', 'p']
escape_key = 'escape'
choice_time_limit = 5
fixation_duration = 1

#stimuli settings
text_color = 'black'
options_x_offset = 200

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
fixed_gamble = TextStim(win=mywin, text='50% chance of winning CHF 600', color=text_color, pos=(-options_x_offset, 0))
changing_gamble = TextStim(win=mywin, color=text_color, pos=(options_x_offset, 0))

fixation_cross = TextStim(win=mywin, text='+', color=text_color)

rewards = np.arange(0, 601, 30)
rewards[0] += 1
n_trials = len(rewards)

#create the dataframe
data = pd.DataFrame([])

#draw the stimuli
trial_routine = Routine(window=mywin, frames_per_second=frames_per_second, escape_key=escape_key)

for t in range(n_trials):
    # put here things that change every trial
    changing_gamble.text = 'a sure gain of  CHF %s' % rewards[t]

    # first event
    trial_routine.wait_for_time_limit(
        components=[fixation_cross], 
        time_seconds=fixation_duration, 
        label='fixation_cross')

    # second event
    key, rt = trial_routine.wait_for_keys_or_time_limit(
        components=[fixed_gamble, changing_gamble], 
        valid_keys=choice_keys, 
        time_seconds=choice_time_limit, 
        label='gamble_choice')
    data = data.append({'rt':rt, 'choice': key, 'trial': t, 'reward': rewards[t]}, ignore_index=True) # record the responses

    #save data to file
    for label in expInfo.keys():
        data[label] = expInfo[label]
    data.to_csv(fileName + '.csv')
    
#cleanup
mywin.close()
core.quit()
