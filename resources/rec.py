import pyautogui
import numpy as np
import time
import imageio
from PIL import ImageDraw, ImageGrab
import win32api

def start_rec(output_file):
    MB1 = False
    MB2 = False

    frames = []
    duration = 15
    fps = 24
    num_frames = duration * fps
    start_time = time.time()

    color = "white"

    for _ in range(num_frames):
        left_state = win32api.GetKeyState(0x01)
        right_state = win32api.GetKeyState(0x02)

        MB1 = (left_state < 0)
        MB2 = (right_state < 0)

        img = ImageGrab.grab(all_screens=True)
        draw = ImageDraw.Draw(img)
        center_x, center_y = pyautogui.position()
        radius = 5

        if MB1:
            color = "red"
        elif MB2:
            color = "yellow"
        else:
            color = "white"

        draw.ellipse([(center_x - radius, center_y - radius), (center_x + radius, center_y + radius)], outline="black", fill=color, width=2)

        frame = np.array(img)
        frames.append(frame)
    imageio.mimsave(output_file, frames, fps=fps, quality=8)