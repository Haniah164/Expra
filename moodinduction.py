import os
import random
import time
import csv
from psychopy import sound, core
import ug_params as params

# CONFIGURATION
MOOD_LIST = ["anger", "sadness", "happiness", "neutral"]
MOOD_DIR = "stimuli"
MUSIC_DURATION = 90
LOG_FILE = "mood_log.csv"

# SELECT RANDOM MOOD
MOOD = random.choice(MOOD_LIST)

# LOAD MUSIC FILE
def load_music(mood):
    mood_path = os.path.join(MOOD_DIR, mood)
    music_files = [f for f in os.listdir(mood_path) if f.endswith((".mp3", ".wav"))]
    if not music_files:
        raise FileNotFoundError
    selected_music = random.choice(music_files)
    return sound.Sound(os.path.join(mood_path, selected_music)), selected_music

# RUN MOOD INDUCTION AND LOG TIMESTAMPS
try:
    music, filename = load_music(MOOD)
    onset_time = time.time()
    music.play()
    core.wait(MUSIC_DURATION)
    music.stop()
    offset_time = time.time()

    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["mood", "audio_file", "onset_time", "offset_time"])
        writer.writerow([MOOD, filename, onset_time, offset_time])

except Exception:
    pass