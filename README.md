# psych-routines
Useful functions for Psychopy, such as routines for precise timing of events/responses in psychological experiments.

The **Routine** class can be used to present stimuli with millisecond-precision, without having to write a loop for the monitor frames. 

To initialize the **Routine** class you only need to specify the window, the number of frames per second, and an escape key, as in the examples:

```python
trial_routine = Routine(window=mywin, frames_per_second=frames_per_second, escape_key=escape_key)
```

It can then be called to time and record responses from different events in the same trial. For example, if the first event is a fixation cross, and the second is a choice between the two options.

```python
# first event
trial_routine.wait_for_time_limit(
    components=[fixation_cross], 
    time_seconds=fixation_duration, 
    label='fixation_cross')
```

This event has a fixed time, so the `wait_for_time_limit` function is called. Here, in the `components` argument, we only present the fixation cross. In general, you would put here all the stimuli you want to be drawn in this event, from the bottom one to the top one. We also then specify the duration of this first event in seconds and a label that is very useful for logging. 

```python
# second event
key, rt = trial_routine.wait_for_keys_or_time_limit(
    components=[fixed_gamble, changing_gamble], 
    valid_keys=choice_keys, 
    time_seconds=choice_time_limit, 
    label='gamble_choice')
```

This event is a bit different, because we want both a time limit for a response, but also to record choices. For this purpose we call the `wait_for_keys_or_time_limit` function. In the components we put both options' stimuli, we then define the time limit and the valide keys (for left and right). And finally a label, as we did in the first event. This event now returns 2 values: `key` and `rt`.