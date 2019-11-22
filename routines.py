from psychopy import core, event, logging
import numpy as np

"""
We have 4 ways of running a routine:
1) for a certain amount of time
2) stop when a response (among possible ones) is given
3) stop when a response (among possible ones) is given or a certain amount of time is expired
4) for a certain amount of time, and also record the first response given (among possible ones)
"""

class Routine(object):
    def __init__(self, window, frames_per_second, escape_key):
        self.frames_per_second = frames_per_second
        self.escape_key = escape_key
        self.window = window
        self.timer = core.Clock()

    def wait_for_time_limit(self, components, time_seconds, label):
        n_frames = self.frames_per_second*time_seconds # define number of frames
        event.clearEvents() # clear event cache
        self.window.logOnFlip(level=logging.EXP, msg='%s onset' % label) # log onset stimuli
        self.window.callOnFlip(self.timer.reset)

        for frameN in range(n_frames):
            for comp in components:
                comp.draw()
            self.window.flip()

            pressed_keys = event.getKeys(keyList=[self.escape_key])
            if len(pressed_keys)>0:
                self.window.close()
                core.quit()

        self.window.logOnFlip(level=logging.EXP, msg='%s offset' % label) # log offset stimuli
        return (time_seconds)

    def wait_for_keys(self, components, valid_keys, label):
        event.clearEvents() # clear event cache
        self.window.logOnFlip(level=logging.EXP, msg='%s onset' % label) # log onset stimuli
        self.window.callOnFlip(self.timer.reset)
        key_list = np.append(valid_keys, self.escape_key)

        while True:
            for comp in components:
                comp.draw()
            self.window.flip()

            pressed_keys = event.getKeys(keyList=key_list, timeStamped=self.timer)
            if len(pressed_keys)>0:
                key, rt = pressed_keys[0] # get the first pressed key and response time

                if key == self.escape_key:
                    self.window.close()
                    core.quit()
                else:
                    break

        self.window.logOnFlip(level=logging.EXP, msg='%s offset' % label) # log offset stimuli
        return key, rt

    def wait_for_keys_or_time_limit(self, components, valid_keys, time_seconds, label):
        n_frames = self.frames_per_second*time_seconds # define number of frames
        event.clearEvents() # clear event cache
        self.window.logOnFlip(level=logging.EXP, msg='%s onset' % label) # log onset stimuli
        self.window.callOnFlip(self.timer.reset)
        key_list = np.append(valid_keys, self.escape_key)

        for frameN in range(n_frames):
            for comp in components:
                comp.draw()
            self.window.flip()

            pressed_keys = event.getKeys(keyList=key_list, timeStamped=self.timer)
            if len(pressed_keys)>0:
                key, rt = pressed_keys[0] # get the first pressed key and response time

                if key == self.escape_key:
                    self.window.close()
                    core.quit()
                else:
                    break

        self.window.logOnFlip(level=logging.EXP, msg='%s offset' % label) # log offset stimuli
        if len(pressed_keys)>0: 
             return key, rt
        else:
             return np.nan, self.timer.getTime()

    def wait_for_time_limit_first_key(self, components, valid_keys, time_seconds, label):
        n_frames = self.frames_per_second*time_seconds # define number of frames
        event.clearEvents() # clear event cache
        self.window.logOnFlip(level=logging.EXP, msg='%s onset' % label) # log onset stimuli
        self.window.callOnFlip(self.timer.reset)
        key_list = np.append(valid_keys, self.escape_key)

        for frameN in range(n_frames):
            for comp in components:
                comp.draw()
            self.window.flip()

            pressed_keys = event.getKeys(keyList=key_list, timeStamped=self.timer)
            if len(pressed_keys)>0:
                key, rt = pressed_keys[0] # get the first pressed key and response time

                if key == self.escape_key:
                    self.window.close()
                    core.quit()

        self.window.logOnFlip(level=logging.EXP, msg='%s offset' % label) # log offset stimuli
        if len(pressed_keys)>0: 
             return key, rt
        else:
             return np.nan, self.timer.getTime()
