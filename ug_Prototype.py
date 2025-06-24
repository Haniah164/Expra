from psychopy import visual, event, core, data, gui, os, sound #import some libraries from PsychoPy
from psychopy.hardware import keyboard
import pandas as pd
import csv
import moodinduction
import mcq
from pathlib import Path
import random
import Generate_Files
random.seed() #Initializing RNG
timer = core.CountdownTimer() #Initializing Timer
global_timer = core.Clock()

exp_info = {'participant_id': '', 'gender': ['Male', 'Female', 'Non-Binary', 'Prefer not to say'], 'age': ''}
dlg = gui.DlgFromDict(dictionary=exp_info, title='Experiment Information')
if not dlg.OK:
    core.quit()

if (int(exp_info['age']) < 18):
    core.quit()

def assignCondition():
    choice = random.choice(params.INSTRUCTION_TYPE)
    print(choice)
    return choice
 
#config:
win = visual.Window([1024, 768], monitor='testMonitor', units='pix', fullscr = True)
CWD = Path.cwd()
trial_number = 0
import ug_params as params
if not (CWD / 'data').exists():
    (CWD / 'data').mkdir()

#Dataframe for UG
df_dict = {
    'participant_id': [''],
    'gender': [''],
    'age': [''],
    'mood': [''],
    'trial_number': [''],
    'agent_type': [''],
    'offer_value': [''],
    'choice': [''],
    'global_time': [''],
    'reaction_time': [''],
    'emotional_response': [''],
    'selected_emotion': [''],
    'confidence_key': ['']
}
df = pd.DataFrame(df_dict)

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
text_testTrial = visual.TextBox2(win=win, text = "Do you understand what you have to do in this experiment? If yes, press 's' to start the experiment. If not, either ask your supervisor or press 't' to start the test-trials again.",
                                            pos=[0, 0], units='height', letterHeight=0.02)
text_feedback = visual.TextBox2(win=win, text = '/', pos=[0, 200])
text_introduction = visual.TextBox2(win=win, text = "In the following experiment you will play a game with another participant. In each round the other player will receive 10 Euros and has to decide how to split those between themselves and you. Then you have to decide if you want to accept the offer. If you accept, each player receives the amount that has been agreed uppon. If you decline the offer, no participant receives something. \n \nAfter a couple of rounds you will be asked a couple questions. Please answer honest. \n \nYou will now play a couple test rounds against the computer to get an idea of what the experiment is about. If you have questions, do not hesitate to ask the supervisor. Thank you for participating in our experiment. Press 't' to start the test trials.",
                                            pos=[0, 0], units='height', letterHeight=0.02)

#create circles
circle0=visual.Circle(win=win, pos=[-100, 0], radius=[5], size=2)
circle1=visual.Circle(win=win, pos=[-80, 0], radius=[5], size=2)
circle2=visual.Circle(win=win, pos=[-60, 0], radius=[5], size=2)
circle3=visual.Circle(win=win, pos=[-40, 0], radius=[5], size=2)
circle4=visual.Circle(win=win, pos=[-20, 0], radius=[5], size=2)
circle5=visual.Circle(win=win, pos=[0,  0], radius=[5], size=2)
circle6=visual.Circle(win=win, pos=[20, 0], radius=[5], size=2)
circle7=visual.Circle(win=win, pos=[40, 0], radius=[5], size=2)
circle8=visual.Circle(win=win, pos=[60, 0], radius=[5], size=2)
circle9=visual.Circle(win=win, pos=[80, 0], radius=[5], size=2)
circles = [circle0, circle1, circle2, circle3, circle4, circle5, circle6, circle7, circle8, circle9]

#create a keyboard component
kb = keyboard.Keyboard()

saved_trial_number = []
saved_agent = []
saved_ratio = []
saved_response = []
saved_global_timer = []
saved_response_time = []

def logTrial(agent, ratio, response, response_time, trial_number):
    saved_trial_number.append(trial_number)
    saved_agent.append(agent)
    saved_ratio.append(ratio)
    saved_response.append(response)
    saved_global_timer.append(global_timer.getTime())
    saved_response_time.append(response_time)
    
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

#def moodInduction():


tracks_played_this_cycle = 0

track_list_sadness = ['.\Audio\rock\24.mp3', '.\Audio\pop\59.mp3', '.\Audio\rock\76.mp3', '.\Audio\rock\42.mp3']


#TODO
def return_audio_path(emotion):
    Generate_Files.getEmotionDf(emotion)
    df_tracks = pd.read_csv("track_emotions.csv')
    tmp = df_tracks.loc[
    return df_tracks
    


def testTrial_Response(response, ratio):
    if response == 'Accepted':
        text_feedback.setText('You would have accepted the offer and received '+str(ratio)+'.')
        text_feedback.setPos([80, 75])
    if response == "Rejected":
        text_feedback.setText('You would have rejected the offer.')
        text_feedback.setPos([120, 75])
    if response == 'Timeout':
        text_feedback.setText('No response in time. Next offer displayed soon. Please respond more quickly.')
        text_feedback.setPos([40, 75])
    text_feedback.draw()
    win.flip()
    timer.reset()
    timer.addTime(params.OUTCOME_SCRREN_TIME_SECONDS)
    while timer.getTime() > 0:
        continue



def testTrials():
    text_introduction.draw()
    win.flip()
    while True:
            kb.clock.reset()
            keys = kb.getKeys(['t'])
            if 't' in keys:
                break
    mood_list = random.sample(params.MOOD_LIST, 4)
    while True:
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
            text_offer.draw()
        
            win.flip()
        
            timer.reset()
            timer.addTime(params.OFFER_SCREEN_TIME_SECONDS)
            while True:
                kb.clock.reset()
                keys = kb.getKeys(['n', 'y', 'q'])
                if 'n' in keys:
                    testTrial_Response('Rejected', ratio)
                    break
                if 'y' in keys:
                    testTrial_Response('Accepted', ratio)
                    break
                if timer.getTime() <= 0:
                    testTrial_Response('Timeout', ratio)
                    break
                event.clearEvents()
        selected_emotion, confidence_key = mcq.emotion_mcq(win)
        #TODO Aks if participant understood the experiment
        text_testTrial.draw()
        win.flip()
        while True:
            kb.clock.reset()
            keys = kb.getKeys(['t', 's'])
            if 't' in keys:
                break
            if 's' in keys:
                return

def mainUG():
    #music.play
    core.wait(15)
    mood_list = random.sample(params.MOOD_LIST, 3)
    for i in range(params.NUM_OF_CYCLES):
        mood = mood_list[i]
        #moodinduction.load_music(mood)
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
                    logTrial(agent_name, ratio, 'Rejected', params.OFFER_SCREEN_TIME_SECONDS-timer.getTime(), trial_number)
                    break
                if 'y' in keys:
                    logTrial(agent_name, ratio, 'Accepted', params.OFFER_SCREEN_TIME_SECONDS-timer.getTime(), trial_number)
                    break
                if timer.getTime() <= 0:
                    logTrial(agent_name, ratio, 'Timeout', params.OFFER_SCREEN_TIME_SECONDS-timer.getTime(), trial_number)
                    break
                event.clearEvents()
        #moodinduction.stop_music(music)
        selected_emotion, confidence_key = mcq.emotion_mcq(win)
        #log results in dataframe
        for trial in range(params.NUM_OF_TRIALS_PER_CYCLE):
            df.loc[len(df)]=[exp_info['participant_id'], exp_info['gender'], exp_info['age'], saved_trial_number[trial],
            mood, saved_agent[trial], saved_ratio[trial], saved_response[trial], saved_global_timer[trial], saved_response_time[trial], '',
            selected_emotion, confidence_key]
    
testTrials()
mainUG()

df.to_csv(exp_info['participant_id']+'-UG-'+data.getDateStr(), index=True, sep='\t')

#stop_wristband_recording()
#debrief()
win.close()
core.quit()