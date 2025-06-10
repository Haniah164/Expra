from psychopy import visual, event
import os
import csv

def emotion_mcq(win, csv_filename):
    
    #Define local response options
    emotions = ['Anger', 'Disgust', 'Sadness', 'Happiness', 'Neutral', 'Anxiety', 'Confusion']
    confidence_scale = ['1', '2', '3', '4', '5']

    #Show emotion MCQ
    emotion_text = 'What emotion do you feel right now?\n\n' + "\n".join(
        f"{i+1}: {e}" for i, e in enumerate(emotions)
    )
    emotion_question = visual.TextStim(win, text=emotion_text, color='white',
                                       height=30, wrapWidth=800)
    emotion_question.draw()
    win.flip()
    emotion_key = event.waitKeys(keyList=[str(i+1) for i in range(len(emotions))])[0]
    selected_emotion = emotions[int(emotion_key) - 1]

    #Show confidence rating
    confidence_text = 'How confident are you in your answer?\n(1 = not confident, 5 = very confident)'
    confidence_question = visual.TextStim(win, text=confidence_text, color='white',
                                          height=30, wrapWidth=800)
    confidence_question.draw()
    win.flip()
    confidence_key = event.waitKeys(keyList=confidence_scale)[0]

    #Append to CSV
    os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
    file_exists = os.path.isfile(csv_filename)
    with open(csv_filename, mode='a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['emotion', 'emotion_key', 'confidence'])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'emotion': selected_emotion,
            'emotion_key': emotion_key,
            'confidence': confidence_key
        })