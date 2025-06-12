import os
import random
import time
import csv
from psychopy import sound, core
import ug_params as params



# LOAD MUSIC FILE
def load_music(mood):
    mood_path = os.path.join(params.MOOD_DIR, mood)
    music_files = [f for f in os.listdir(mood_path) if f.endswith(('.mp3', '.wav'))]
    if not music_files:
        raise FileNotFoundError
    selected_music = random.choice(music_files)
    return sound.Sound(os.path.join(mood_path, selected_music)), selected_music

# RUN MOOD INDUCTION AND LOG TIMESTAMPS
def play_music(mood, global_time):
    try:
        music, filename = load_music(mood)
        music.play()

        with open(params.LOG_FILE, mode="a", newline="") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
            if file.tell() == 0:
                writer.writerow(['mood', 'audio_file', 'onset_time'])
            writer.writerow([mood, filename, global_time])

    except Exception:
        pass
    return music
    
def stop_music(music):
    music.stop()
    