from psychopy import visual, core, event, data, gui
import random
import csv
import os


# === Experiment Setup ===
exp_info = {'participant': ''}
dlg = gui.DlgFromDict(dictionary=exp_info, title='Emotion MCQ Task')
if not dlg.OK:
    core.quit()

filename = f"data/{exp_info['participant']}_emotionMCQ.csv"
os.makedirs("data", exist_ok=True)

win = visual.Window([1000, 700], color='black', units='pix')

# === Questions and Options ===
emotions = ['Anger', 'Disgust', 'Sadness', 'Happiness', 'Neutral', 'Surprise', 'Confusion', 'Fear']
confidence_scale = ['1', '2', '3', '4', '5']

emotion_question = visual.TextStim(win, text='What emotion do you feel right now?\n\n' +
                                    '\n'.join([f"{i+1}: {e}" for i, e in enumerate(emotions)]),
                                    color='white', height=30, wrapWidth=800)

confidence_question = visual.TextStim(win, text='How confident are you in your answer?\n(1 = not confident, 5 = very confident)',
                                      color='white', height=30, wrapWidth=800)

instruction_text = visual.TextStim(win, text='Press any key to start.', color='white', height=30)

# === Start ===
instruction_text.draw()
win.flip()
event.waitKeys()

# === Trial Loop ===
n_trials = 12  # simulate 12 trials to show emotion MCQ on every 4th trial
trial_data = []

for trial in range(1, n_trials + 1):
    trial_dict = {'trial_number': trial}

    if trial % 4 == 0:
        # === Emotion Question ===
        emotion_question.draw()
        win.flip()
        emotion_key = event.waitKeys(keyList=[str(i+1) for i in range(len(emotions))])[0]
        selected_emotion = emotions[int(emotion_key) - 1]
        trial_dict['emotion'] = selected_emotion
        trial_dict['emotion_key'] = emotion_key

        # === Confidence Question ===
        confidence_question.draw()
        win.flip()
        confidence_key = event.waitKeys(keyList=confidence_scale)[0]
        trial_dict['confidence'] = confidence_key
    else:
        trial_dict['emotion'] = ''
        trial_dict['emotion_key'] = ''
        trial_dict['confidence'] = ''

    trial_data.append(trial_dict)
    core.wait(0.5)  # inter-trial pause

# === Save Data ===
with open(filename, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['trial_number', 'emotion', 'emotion_key', 'confidence'])
    writer.writeheader()
    writer.writerows(trial_data)

# === End Screen ===
end_text = visual.TextStim(win, text='Task complete. Thank you!', color='white', height=30)
end_text.draw()
win.flip()
event.waitKeys()

win.close()
core.quit()
