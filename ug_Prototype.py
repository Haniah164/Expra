from psychopy import visual, event, core, data, gui, os #import some libraries from PsychoPy
from psychopy.hardware import keyboard
import pandas as pd
import csv
import moodinduction
import mcq
from pathlib import Path
import random
random.seed() #Initializing RNG
timer = core.CountdownTimer() #Initializing Timer
global_timer = core.Clock()

exp_info = {'participant_id': ''}
dlg = gui.DlgFromDict(dictionary=exp_info, title='Experiment Information')
if not dlg.OK:
    core.quit()

def assignCondition():
    choice = random.choice(params.INSTRUCTION_TYPE)
    print(choice)
    return choice
 
#config:
win = visual.Window([1024, 768], monitor='testMonitor', units='pix')
CWD = Path.cwd()
trial_number = 0
import ug_params as params
if not (CWD / 'data').exists():
    (CWD / 'data').mkdir()

#Dataframe for UG
df_dict = {
    'participant_id': [''],
    'mood': [''],
    'trial_number': [''],
    'agent_type': [''],
    'offer_value': [''],
    'choice': [''],
    'global_time': [''],
    'reaction_time': [''],
    'emotional_response': ['']
}
df = pd.DataFrame(df_dict)

#Dataframe for MCQ
df_dict_mcq = {
    'participant_id': [''],
    'emotion': [''],
    'confidence': ['']
}

df_mcq = pd.DataFrame(df_dict_mcq)

condition = assignCondition()
#TODO: Initialize wristband

#create main textbox
text_Main = visual.TextBox2(win=win, text = "Read the proposed offer carefully and decide if you want to accept:",
                                            pos=[0, 300])
text_accept = visual.TextBox2(win=win, text = "Press 'y' to accept the offer.",
                                            pos=[-200, -80], borderColor=["Lime"], size=[250, 70])
text_decline = visual.TextBox2(win=win, text = "Press 'n' to accept the offer.",
                                            pos=[230, -80], borderColor=["Red"], size=[250, 70])
text_closing = visual.TextBox2(win=win, text = "Press 'q' to leave the experiment.", pos=[450, -350])
text_offer = visual.TextBox2(win=win, text = "/", pos=[100, 75])
text_score = visual.TextBox2(win=win, text = "Score: 0", pos=[300, -350])

#create circles
circle0=visual.Circle(win=win, pos=[-50, 0], radius=[5])
circle1=visual.Circle(win=win, pos=[-40, 0], radius=[5])
circle2=visual.Circle(win=win, pos=[-30, 0], radius=[5])
circle3=visual.Circle(win=win, pos=[-20, 0], radius=[5])
circle4=visual.Circle(win=win, pos=[-10, 0], radius=[5])
circle5=visual.Circle(win=win, pos=[0,  0], radius=[5])
circle6=visual.Circle(win=win, pos=[10, 0], radius=[5])
circle7=visual.Circle(win=win, pos=[20, 0], radius=[5])
circle8=visual.Circle(win=win, pos=[30, 0], radius=[5])
circle9=visual.Circle(win=win, pos=[40, 0], radius=[5])
circles = [circle0, circle1, circle2, circle3, circle4, circle5, circle6, circle7, circle8, circle9]

#create a keyboard component
kb = keyboard.Keyboard()

def logTrial(agent, ratio, response, response_time, trial_number):
    df.loc[len(df)]=[exp_info['participant_id'], mood, trial_number, agent, ratio, response, global_timer.getTime(), response_time, '']
    text_feedback = visual.TextBox2(win=win, text = '/', pos=[95, 75])
    
    trial_number = trial_number + 1
    if response == 'Accepted':
        text_feedback.setText('You accepted the offer and received '+str(ratio)+'.')
        text_feedback.setPos([80, 75])
    if response == "Rejected":
        text_feedback.setText('You rejected the offer.')
        text_feedback.setPos([120, 75])
    if response == 'Timeout':
        text_feedback.setText('No response in time. Next offer displayed soon')
        text_feedback.setPos([40, 75])
    text_feedback.draw()
    win.flip()
    timer.reset()
    timer.addTime(params.OUTCOME_SCRREN_TIME_SECONDS)
    while timer.getTime() > 0:
        continue

score = 0 #Potentially no score?

#Initiate mood induction and set emotion: (will later set emotion = ...
#def moodInduction():
mood = "BLANK"

def mainUG():
    mood_list = random.sample(params.MOOD_LIST, 4)
    for i in range(params.NUM_OF_CYCLES):
        mood = mood_list[i]
        #moodinduction.load_music(mood)
        #music = moodinduction.play_music(mood, global_time)
        for j in range(params.NUM_OF_TRIALS_PER_CYCLE):
            agent = random.choice(params.AGENTS)
            agent_name = 'FAIR_AGENT'
            if (agent[0] == 3):
                agent_name = 'NEUTRAL_AGENT'
            if (agent[0] == 1):
                agent_name = 'UNFAIR_AGENT'
            ratio = random.choice(agent)
            text_offer.setText('You recieve '+str(ratio)+', they recieve '+str(10-ratio))
            text_score.setText('Score: '+str(score))
            for x in range(10): #Providing viusal representation
                if x+1 <= ratio:
                    circles[x].setFillColor('Orange')
                else:
                    circles[x].setFillColor('Black')
                circles[x].draw()
            
            text_Main.draw()
            text_accept.draw()
            text_decline.draw()
            text_closing.draw()
            text_offer.draw()
            text_score.draw()
        
            win.flip()
        
            timer.reset()
            timer.addTime(params.OFFER_SCREEN_TIME_SECONDS)
            while True:
                kb.clock.reset()
                keys = kb.getKeys(['n', 'y', 'q'])
                if 'q' in keys:
                    core.quit()
                if 'n' in keys:
                    logTrial(agent_name, ratio, 'Rejected', timer.getTime(), trial_number)
                    break
                if 'y' in keys:
                    logTrial(agent_name, ratio, 'Accepted', timer.getTime(), trial_number)
                    break
                if timer.getTime() <= 0:
                    logTrial(agent_name, ratio, 'Timeout', timer.getTime(), trial_number)
                    break
                event.clearEvents()
        #moodinduction.stop_music(music)
        mcq.emotion_mcq(win, df_mcq, exp_info['participant_id'])
    
mainUG()

df.to_csv(exp_info['participant_id']+'-UG-'+data.getDateStr(), index=True, sep='\t')
df_mcq.to_csv(exp_info['participant_id']+'-MCQ-'+data.getDateStr(), index=True, sep='\t')
#stop_wristband_recording()
#debrief()
win.close()
core.quit()