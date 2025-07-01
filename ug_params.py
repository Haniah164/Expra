# UG Params
OFFER_SCREEN_TIME_SECONDS = 10
OUTCOME_SCRREN_TIME_SECONDS = 1
NUM_OF_CYCLES = 6
NUM_OF_TRIALS_PER_CYCLE = 4
ONSET_TIME_MUSIC = 15
block1 = [1, 3, 5, 2]
block2 = [6, 1, 2, 3]
block3 = [4, 1, 2, 3]
block4 = [3, 1, 2, 3]
blocks = [block1, block2, block3, block4]

# General Params
INSTRUCTION_TYPE = ["Emotion_Focused", "Neutral"]

# Agent Offers
FAIR_AGENT = [5, 6] #Entry is ratio player recieves
NEUTRAL_AGENT = [3, 4, 5, 6]
UNFAIR_AGENT = [1, 2, 3]
AGENTS = [FAIR_AGENT, NEUTRAL_AGENT, UNFAIR_AGENT]

# MCQ Params
EMOTIONS = ['Anger', 'Disgust', 'Sadness', 'Happiness', 'Neutral', 'Anxiety', 'Confusion']
CONFIDENCE_SCALE = ['1', '2', '3', '4', '5']

# Mood Induction Params
MOOD_LIST = ["tension", "sadness", "joyful_activation","tension", "sadness", "joyful_activation"]
MOOD_DIR = "stimuli"
MUSIC_DURATION = 90
LOG_FILE = "mood_log.csv"