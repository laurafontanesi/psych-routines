from __future__ import division
from psychopy.visual import TextStim, ImageStim, Window
from psychopy import core, event, gui, data, logging
import numpy as np
import pandas as pd
import os

from routines import Routine

# Code for the feedback experiment of Spiering & Ashby (2008) https://doi.org/10.1111/j.1467-9280.2008.02219.x

#general settings
expName = 'example_3'
screen_size = [800, 600]
frames_per_second = 60
full_screen = False
background_color = '#bfbfbf'

# trial settings
choice_keys = ['a', 'b']
escape_key = 'escape'
fixation_duration = 1.5
choice_timeout = 5
messages_duration = .5
message_beginning_duration = 5

#stimuli settings
image_size = 100
text_correct_color = 'blue'
text_incorrect_color = 'red'
text_too_slow = 'black'
text_beginning_block = 'black'
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
"""
2 separate blocks: learning (difficulty either increases or decreases) & transfer (difficulty are all shuffled) blocks
1 group of subjects starts with easy to hard (odd participants) and the other group starts with hard to easy (even participants) in the learning block
both leanring block and transfer are 30 trials, so 60 trials in total
"""

directory_stimuli = os.path.join(os.getcwd(), 'stimuli', 'example_3') # directory where images can be found
patch_image = ImageStim(win=mywin,  size=image_size) # create image object
n_trials = 30

if (expInfo['participant'] % 2) == 0: # order difficulty even participants
    order_difficulty = ['hard', 'medium', 'easy'] 
else: # order difficulty odd participants
    order_difficulty = ['easy', 'medium', 'hard'] 

"""
create a dataframe with information about the stimuli corrisponding to their file number:
- the first half of images are from category 'A', the second from 'B'
- for the first half of images the correct response is 'a', for the second is 'b'
- difficulty goes from easy to medium to hard, every 5 images for both category

example: image 1 (patch1.png) is from category A, so the correct response is 'a' and the difficulty is easy
"""
stimuli = pd.DataFrame(
    {'image_number': range(1, 31),
     'category': np.repeat(['A', 'B'], repeats=15),
     'correct_response': np.repeat(choice_keys, repeats=15),
     'difficulty': pd.Categorical(np.tile(np.repeat(['easy', 'medium', 'hard'], repeats=5), 2), categories=order_difficulty), # make it a categorical object to order it
    })
print(stimuli)

n_blocks = 2
transfer_block = stimuli.sample(frac=1).reset_index(drop=True) # shuffle stimuli across difficulty levels
learning_block = stimuli.groupby(['difficulty']).apply(lambda x: x.sample(frac=1)).reset_index(drop=True) # shuffle stimuli by difficulty level
blocks = [learning_block, transfer_block] # blocks order
print(learning_block)

correct_message = TextStim(win=mywin, text="Correct!", color=text_correct_color, height=text_height)
incorrect_message = TextStim(win=mywin, text="Incorrect!", color=text_incorrect_color, height=text_height)
too_slow_message = TextStim(win=mywin, text="Too slow!", color=text_too_slow, height=text_height)

beginning_learning_block_message = TextStim(win=mywin, text="A block of trials will start now. Here, you will receive feedback after each choice you made.", color=text_beginning_block, height=text_height)
beginning_transfer_block_message = TextStim(win=mywin, text="A block of trials will start now. Here, you will no longer receive feedback.", color=text_beginning_block, height=text_height)
messages_beginning = [beginning_learning_block_message, beginning_transfer_block_message]

end_transfer_message = TextStim(win=mywin, color=text_beginning_block, height=text_height)

#create the dataframe
data = pd.DataFrame([])

#draw the stimuli
trial_routine = Routine(window=mywin, frames_per_second=frames_per_second, escape_key=escape_key)

for bl in range(n_blocks):
    block = blocks[bl]

    trial_routine.wait_for_time_limit(
            components=[messages_beginning[bl]], 
            time_seconds=message_beginning_duration, 
            label='message_beginning')

    for t in range(n_trials):
        # put here things that change at the beginning of every trial
        image_trial = 'patch{}.png'.format(block['image_number'][t])
        correct_resp_trial = block['correct_response'][t]
        patch_image.image = os.path.join(directory_stimuli, image_trial)

        # first event
        trial_routine.wait_for_time_limit(
            components=[], 
            time_seconds=fixation_duration, 
            label='fixation_cross')

        # second event
        key, rt = trial_routine.wait_for_keys_or_time_limit(
            components=[patch_image],
            time_seconds=choice_timeout,
            valid_keys=choice_keys,
            label='patch_choice')
        
        # third event
        if rt >= choice_timeout: # if no response was given (key == np.nan is also ok)
            accuracy_trial = np.nan
            message = too_slow_message
        elif key == correct_resp_trial: # if the correct response was given
            accuracy_trial = 1
            message = correct_message
        else: # if the incorrect response was given
            accuracy_trial = 0
            message = incorrect_message
        
        if bl == 0: # only give a message in the learning block
            trial_routine.wait_for_time_limit(
                components=[message], 
                time_seconds=messages_duration, 
                label='choice_feedback')

        data = data.append(
            {'trial':int(t+1), 'rt':rt, 'choice':key, 'accuracy':accuracy_trial, 'image':image_trial, 'block':['learning', 'transfer'][bl],
             'difficulty':block['difficulty'][t], 'correct_response':correct_resp_trial, 'category':block['category'][t]},
            ignore_index=True) # record the responses

        #save data to file
        for label in expInfo.keys():
            data[label] = expInfo[label]
        data.to_csv(fileName + '.csv')

# final message with accuracy feedback
accuracy_learning = int(data.loc[data.block == 'learning', 'accuracy'].mean()*100)
accuracy_transfer = int(data.loc[data.block == 'transfer', 'accuracy'].mean()*100)

end_transfer_message.text = "Congratulations, you finished the experiment. You accuracy was {}% in the learning part and {}% in the test.".format(accuracy_learning, accuracy_transfer)
trial_routine.wait_for_time_limit(
        components=[end_transfer_message], 
        time_seconds=message_beginning_duration, 
        label='message_end')

#cleanup
mywin.close()
core.quit()