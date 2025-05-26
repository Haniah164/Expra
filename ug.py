from psychopy import visual, event, core #import some libraries from PsychoPy
from psychopy.hardware import keyboard
import random
random.seed()
 
#config:
win = visual.Window([1024, 768], monitor="testMonitor", units="pix")
num_trials = 40
agents = ["fair", "neutral", "unfair"]
 
#create main textbox
text_Main = visual.TextBox2(win=win, text = "Read the proposed offer carefully and decide if you want to accept:", pos=[10, 80])

#create a keyboard component
kb = keyboard.Keyboard()


#draw the stimuli and update the window
while True: #this creates a never-ending loop
    random_agents = random.choice(agents)
    text_Main.draw()
    win.flip()

    if len(kb.getKeys()) > 0:
        break
    event.clearEvents()

#cleanup
win.close()
core.quit()