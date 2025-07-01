from psychopy import visual, event
import os
import pandas as pd
import csv
import ug_params as params
import random
random.seed()


def emotion_mcq(win):
    randomized_emotions = random.sample(params.EMOTIONS, k=len(params.EMOTIONS))
    print(randomized_emotions)
    #Show emotion MCQ
    emotion_text = 'What emotion do you feel right now? Press the corresponding key to answer.\n\n' + "\n".join(
        f"{i+1}: {e}" for i, e in enumerate(randomized_emotions)
    )
    emotion_question = visual.TextStim(win, text=emotion_text, color='white',
                                       height=30, wrapWidth=800)
    emotion_question.draw()
    win.flip()
    emotion_key = event.waitKeys(keyList=[str(i+1) for i in range(len(params.EMOTIONS))])[0]
    selected_emotion = randomized_emotions[int(emotion_key) - 1]

    #Show confidence rating
    confidence_text = 'How strong are you experiencing this emotion?\n(Press 1 = low intensity to 5 = high intensity)'
    confidence_question = visual.TextStim(win, text=confidence_text, color='white',
                                          height=30, wrapWidth=800)
    confidence_question.draw()
    win.flip()
    confidence_key = event.waitKeys(keyList=params.CONFIDENCE_SCALE)[0]
    
    return selected_emotion, confidence_key