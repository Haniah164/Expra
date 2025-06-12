from psychopy import visual, event, core, data, gui
import os
import csv

class CSV_EXP:
    participant_id: str
    dataDir: str
    file_name: str
    file_path: str

    def __init__(self, participant_id: str, dataDir: str):
        self.participant_id = participant_id
        self.dataDir = dataDir
        self.file_name = "data/" + participant_id + data.getDateStr()
        self.file_path = os.path.join(dataDir, file_name)

    def create_csv():
        with open(file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["participant_ID, mood, trial_nr, agent_type, offer_value, choice, RT, emotion_response, time"])
        return 
        
    def add_trial_to_csv(trialHistory: list):
        with open(file_path, "a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(trialHistory)
        return
