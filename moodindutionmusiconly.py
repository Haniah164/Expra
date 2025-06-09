import os
import random
from psychopy import sound, core
import ug_params as params

# CONFIGURATION
MOOD_LIST = ["anger", "sadness", "happiness", "neutral"]
MOOD_DIR = "stimuli"
MUSIC_DURATION = 90

# RANDOMLY SELECT MOOD
MOOD = random.choice(MOOD_LIST)

# LOAD MUSIC FOR MOOD
def load_music(mood):
    mood_path = os.path.join(MOOD_DIR, mood)
    music_files = [f for f in os.listdir(mood_path) if f.endswith((".mp3", ".wav"))]
    if not music_files:
        raise FileNotFoundError
    selected_music = random.choice(music_files)
    return sound.Sound(os.path.join(mood_path, selected_music))

# PLAY MUSIC FOR MOOD
try:
    music = load_music(MOOD)
    music.play()
    core.wait(MUSIC_DURATION)
    music.stop()
except Exception:
    pass