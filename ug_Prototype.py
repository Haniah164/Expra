import pygame
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

# Change mainPath before experiment
#----------------------------------------------------------------------------------
mainPath = 'C:\\Users\\timon\OneDrive\\Dokumente\\Uni Darmstadt\\4.Semester\\Expra'
#----------------------------------------------------------------------------------


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
    'offer_value': [''],
    'choice': [''],
    'global_time': [''],
    'reaction_time': [''],
    'selected_emotion': [''],
    'confidence_key': ['']
}
df = pd.DataFrame(df_dict)

condition = assignCondition()


#create main textbox
text_Main = visual.TextBox2(win=win, text = "Read the proposed offer carefully and decide if you want to accept:",
                                            pos=[0, 300])
text_accept = visual.TextBox2(win=win, text = "Press 'y' to accept the offer.",
                                            pos=[-200, -80], borderColor=["Lime"], size=[250, 70])
text_decline = visual.TextBox2(win=win, text = "Press 'n' to accept the offer.",
                                            pos=[230, -80], borderColor=["Red"], size=[250, 70])
text_closing = visual.TextBox2(win=win, text = "Press 'q' to leave the experiment.", pos=[450, -350])
text_offer = visual.TextBox2(win=win, text = "/", pos=[100, 75])
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

saved_agent = []
saved_ratio = []
saved_response = []
saved_global_timer = []
saved_response_time = []

def logTrial(ratio, response, response_time, trial_number):
    saved_ratio.append(ratio)
    saved_response.append(response)
    saved_global_timer.append(global_timer.getTime())
    saved_response_time.append(response_time)
    
    if response == 'Accepted':
        text_feedback.setText('You accepted the offer and received '+str(ratio)+'.')
        text_feedback.setPos([80, 75])
    if response == "Rejected":
        text_feedback.setText('You rejected the offer.')
        text_feedback.setPos([150, 75])
    if response == 'Timeout':
        text_feedback.setText('No response in time. Next offer displayed soon')
        text_feedback.setPos([40, 75])
    text_feedback.draw()
    win.flip()
    timer.reset()
    timer.addTime(params.OUTCOME_SCRREN_TIME_SECONDS)
    while timer.getTime() > 0:
        continue


track_list_sadness = pd.read_csv('sadness_tracks.csv')
track_list_joy = pd.read_csv('joyful_activation_tracks.csv')
track_list_tension = pd.read_csv('tension_tracks.csv')

def return_audio_path(emotion):
    if emotion == 'tension':
        track_nr = random.randint(2, 12)
        return track_list_tension.iat[track_nr, 3]
    if emotion == 'joyful_activation':
        track_nr = random.randint(2, 10)
        return track_list_joy.iat[track_nr, 3]
    if emotion == 'sadness':
        track_nr = random.randint(2, 11)
        return track_list_sadness.iat[track_nr, 3]
    return None

music = sound.Sound(mainPath + return_audio_path('sadness'))

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
    random_blocks = random.sample(params.blocks, 4)
    for i in range(3):
        mood = params.MOOD_LIST[i]
        print(mood)
        print(return_audio_path(mood))
        music.setSound(return_audio_path(mood))
        music.play()
        win.flip()
        core.wait(params.ONSET_TIME_MUSIC)
        for j in range(params.NUM_OF_TRIALS_PER_CYCLE):
            random_trials = random.sample(random_blocks[j], 4)
            ratio = random_trials[j]
            text_offer.setText('You recieve '+str(ratio)+', they recieve '+str(10-ratio))
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
        
            win.flip()
        
            timer.reset()
            timer.addTime(params.OFFER_SCREEN_TIME_SECONDS)
            while True:
                kb.clock.reset()
                keys = kb.getKeys(['n', 'y', 'q'])
                if 'q' in keys:
                    core.quit()
                if 'n' in keys:
                    logTrial(ratio, 'Rejected', params.OFFER_SCREEN_TIME_SECONDS-timer.getTime(), trial_number)
                    break
                if 'y' in keys:
                    logTrial(ratio, 'Accepted', params.OFFER_SCREEN_TIME_SECONDS-timer.getTime(), trial_number)
                    break
                if timer.getTime() <= 0:
                    logTrial(ratio, 'Timeout', params.OFFER_SCREEN_TIME_SECONDS-timer.getTime(), trial_number)
                    break
                event.clearEvents()
        selected_emotion, confidence_key = mcq.emotion_mcq(win)
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
    random_blocks = random.sample(params.blocks, 4)
    last_music_onset = global_timer.getTime()
    for i in range(params.NUM_OF_CYCLES):
        mood = params.MOOD_LIST[i]
        print(mood)
        print(return_audio_path(mood))
        music.setSound(return_audio_path(mood))
        music.play()
        win.flip()
        core.wait(params.ONSET_TIME_MUSIC)
        for j in range(params.NUM_OF_TRIALS_PER_CYCLE):
            random_trials = random.sample(random_blocks[j], 4)
            ratio = random_trials[j]
            text_offer.setText('You recieve '+str(ratio)+', they recieve '+str(10-ratio))
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
        
            win.flip()
        
            timer.reset()
            timer.addTime(params.OFFER_SCREEN_TIME_SECONDS)
            while True:
                kb.clock.reset()
                keys = kb.getKeys(['n', 'y', 'q'])
                if 'q' in keys:
                    core.quit()
                if 'n' in keys:
                    logTrial(ratio, 'Rejected', params.OFFER_SCREEN_TIME_SECONDS-timer.getTime(), trial_number)
                    break
                if 'y' in keys:
                    logTrial(ratio, 'Accepted', params.OFFER_SCREEN_TIME_SECONDS-timer.getTime(), trial_number)
                    break
                if timer.getTime() <= 0:
                    logTrial(ratio, 'Timeout', params.OFFER_SCREEN_TIME_SECONDS-timer.getTime(), trial_number)
                    break
                event.clearEvents()
        #moodinduction.stop_music(music)
        selected_emotion, confidence_key = mcq.emotion_mcq(win)
        #log results in dataframe
        for trial in range(params.NUM_OF_TRIALS_PER_CYCLE):
            df.loc[len(df)]=[exp_info['participant_id'], exp_info['gender'], exp_info['age'],
            mood, saved_ratio[trial], saved_response[trial], saved_global_timer[trial], saved_response_time[trial],
            selected_emotion, confidence_key]
    
#testTrials()
mainUG()

df.to_csv(exp_info['participant_id']+'-UG-'+data.getDateStr(), index=True, sep='\t')

#stop_wristband_recording()
#debrief()
win.close()
core.quit()