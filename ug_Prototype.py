from psychopy import visual, event, core #import some libraries from PsychoPy
from psychopy.hardware import keyboard
import yaml
from pathlib import Path
import random
random.seed() #Initializing RNG
timer = core.CountdownTimer() #Initializing Timer

def assignCondition():
    choice = random.choice(params.INSTRUCTION_TYPE)
    print(choice)
    return choice
 
#config:
win = visual.Window([1024, 768], monitor="testMonitor", units="pix")
CWD = Path.cwd()
import ug_params as params
if not (CWD / "data").exists():
    (CWD / "data").mkdir()
out_file = (CWD / "data" / f"UG_experiment_'seed'.csv")

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

#create circle 
circle1=visual.Circle(win=win, pos=[-50, 0], radius=[5])
circle2=visual.Circle(win=win, pos=[-40, 0], radius=[5])
circle3=visual.Circle(win=win, pos=[-30, 0], radius=[5])
circle4=visual.Circle(win=win, pos=[-20, 0], radius=[5])
circle5=visual.Circle(win=win, pos=[-10, 0], radius=[5])
circle6=visual.Circle(win=win, pos=[0, 0], radius=[5])
circle7=visual.Circle(win=win, pos=[10, 0], radius=[5])
circle8=visual.Circle(win=win, pos=[20, 0], radius=[5])
circle9=visual.Circle(win=win, pos=[30, 0], radius=[5])
circle10=visual.Circle(win=win, pos=[40, 0], radius=[5])
circles = [circle1, circle2, circle3, circle4, circle5, circle6, circle7, circle8, circle9, circle10]

#create a keyboard component
kb = keyboard.Keyboard()

def logTrial(agent, ratio, response):
    text_feedback = visual.TextBox2(win=win, text = "/", pos=[95, 75])
    #TODO: Log trial in dataframe/CSV
    if response == "Accepted":
        text_feedback.setText("You accepted the offer and received "+str(ratio)+".")
        text_feedback.setPos([80, 75])
    if response == "Rejected":
        text_feedback.setText("You rejected the offer.")
        text_feedback.setPos([120, 75])
    if response == "Timeout":
        text_feedback.setText("No response in time. Next offer displayed soon")
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
emotion = ""

def mainUG():
    for i in range(params.NUM_OF_CYCLES):
        random_agents = random.sample(params.AGENTS, 3)
        
        for agent in random_agents:
            ratio = random.choice(agent)
            text_offer.setText("You recieve "+str(ratio)+", they recieve "+str(10-ratio))
            text_score.setText("Score: "+str(score))
            for x in range(10): #Providing viusal representation
                if x+1 <= ratio:
                    circles[x].setFillColor("Orange")
                else:
                    circles[x].setFillColor("Black")
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
                    logTrial(agent, ratio, "Rejected")
                    break
                if 'y' in keys:
                    logTrial(agent, ratio, "Accepted")
                    break
                if timer.getTime() <= 0:
                    logTrial(agent, ratio, "Timeout")
                    break
                event.clearEvents()
        #Start mCQ()
    
mainUG()
#confidenceRating()

#cleanup
#stop_wristband_recording()
#debrief()
win.close()
core.quit()