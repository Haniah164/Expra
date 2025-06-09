from psychopy import visual, core, sound, event
import os
import random
import time
from datetime import datetime
import ug_params.py

WIN_SIZE = [1024, 768]
IMAGE_DURATION = 6  # seconds
MOOD_DIR = "stimuli"  # folder with subfolders for each mood

win = visual.Window(WIN_SIZE, color="black", fullscr=False, units="pix")

def load_images_and_music(mood_folder):
    "load image paths and the music file for the given mood"
    files = os.listdir(mood_folder)
    images = [os.path.join(mood_folder, f) for f in files if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    music_files = [f for f in files if f.lower().endswith('.mp3') or f.lower().endswith('.wav')]
    music_path = os.path.join(mood_folder, music_files[0]) if music_files else None
    return images, music_path

def show_images(images, duration, log_list):
    "display each image for a fixed duration"
    random.shuffle(images)
    for img_path in images:
        image_stim = visual.ImageStim(win, image=img_path)
        image_stim.draw()
        win.flip()
        start = time.time()
        log_list.append((os.path.basename(img_path), "onset", start))
        core.wait(duration)
        log_list.append((os.path.basename(img_path), "offset", time.time()))

def run_mood_induction_block(mood):
    "run full mood induction for one block"
    print(f"starting mood block: {mood}")
    block_log = []

    mood_folder = os.path.join(MOOD_DIR, mood)
    images, music_path = load_images_and_music(mood_folder)
    images = images[:5]  # max 5 images

    # start music (non-blocking)
    if music_path:
        music = sound.Sound(music_path)
        music.play()
        block_log.append(("music", "start", time.time()))

    # show images
    show_images(images, IMAGE_DURATION, block_log)

    # wait until music ends or timeout (max 90s total)
    core.wait(90 - len(images) * IMAGE_DURATION)
    block_log.append(("music", "stop", time.time()))

    # clear screen
    win.flip()
    core.wait(0.5)

    return block_log

# run multiple blocks

def main():
    moods = ["anger", "disgust", "sadness", "happiness", "neutral"]
    random.shuffle(moods)  # randomized block order

    full_log = []
    for mood in moods:
        log = run_mood_induction_block(mood)
        full_log.append((mood, log))

        # optional break between blocks
        break_text = visual.TextStim(win, text="short break, press SPACE to continue", color="white")
        break_text.draw()
        win.flip()
        event.waitKeys(keyList=["space"])
        win.flip()

    # save logs
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    with open(f"mood_induction_log_{timestamp}.txt", "w") as f:
        for mood, block_log in full_log:
            f.write(f"BLOCK: {mood}\n")
            for entry in block_log:
                name, event_type, t = entry
                f.write(f"{name}\t{event_type}\t{t:.3f}\n")
            f.write("\n")

    print("mood induction complete")
    win.close()
    core.quit()