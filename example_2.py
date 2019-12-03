from __future__ import division
from psychopy.visual import TextStim, Window
from psychopy import core, event, gui, data, logging
import numpy as np
import pandas as pd
import os

from routines import Routine

# Code for the choice titration experiment of Weber and Chapman (2005) https://doi.org/10.1016/j.obhdp.2005.01.001

#general settings
expName = 'example_2'
screen_size = [800, 600]
frames_per_second = 60
full_screen = False
background_color = '#bfbfbf'

# trial settings
choice_keys = ['a', 'l']
escape_key = 'escape'
fixation_duration = .5

#stimuli settings
text_color = 'black'
options_x_offset = 200
text_height = 20

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
safe_gamble = TextStim(win=mywin, color=text_color, pos=(-options_x_offset, 0), height=text_height)
risky_gamble = TextStim(win=mywin, text="10% chance of CHF 3000", color=text_color, pos=(options_x_offset, 0), height=text_height)

n_trials = 50 # max number of trials...
value_current = 1500
value_upper = 3000
value_lower = 0

#create the dataframe
data = pd.DataFrame([])

#draw the stimuli
trial_routine = Routine(window=mywin, frames_per_second=frames_per_second, escape_key=escape_key)

for t in range(n_trials):
    # put here things that change at the beginning of every trial
    value_current = int(np.round(np.mean([value_upper, value_lower])))
    safe_gamble.text = "100% chance of CHF {}".format(value_current)

    # first event
    trial_routine.wait_for_time_limit(
        components=[], 
        time_seconds=fixation_duration, 
        label='fixation_cross')

    # second event
    key, rt = trial_routine.wait_for_keys(
        components=[safe_gamble, risky_gamble],
        valid_keys=choice_keys,
        label='gamble_choice')
    data = data.append(
        {'rt':rt, 'choice': key, 'trial': t, 'current': value_current, 'upper': value_upper, 'lower': value_lower, 'difference':value_upper-value_lower}, 
        ignore_index=True) # record the responses

    #save data to file
    for label in expInfo.keys():
        data[label] = expInfo[label]
    data.to_csv(fileName + '.csv')
    
    # put here things that change at the end of every trial
    if key == choice_keys[0]:
        value_upper = value_current
    elif key == choice_keys[1]:
        value_lower = value_current
    
    # stop experiment when:
    if (value_upper-value_lower) < 25:
        break

#cleanup
mywin.close()
core.quit()
