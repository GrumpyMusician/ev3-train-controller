#!/usr/bin/env pybricks-micropython
import os
import time
from pybricks.hubs import EV3Brick
from pybricks.parameters import Button

ev3 = EV3Brick()

TRAINS_DIR = "programs"
CALIBRATION_DIR = "calibration"

files = []

# Load programs first
try:
    files.extend([
        (TRAINS_DIR, f)
        for f in os.listdir(TRAINS_DIR)
        if f.endswith(".py")
    ])
except OSError:
    pass

# Then calibration programs
try:
    files.extend([
        (CALIBRATION_DIR, f)
        for f in os.listdir(CALIBRATION_DIR)
        if f.endswith(".py")
    ])
except OSError:
    pass

if not files:
    ev3.screen.print("No .py files found!")
    raise SystemExit

MAX_VISIBLE = 5  # How many items are shown at once


def draw_menu(index, scroll_offset):
    ev3.screen.clear()
    title_y = 0
    line_height = 21
    ev3.screen.draw_text(0, title_y, "Select a Program:")

    for i in range(MAX_VISIBLE):
        actual_index = scroll_offset + i
        if actual_index >= len(files):
            break

        folder, filename = files[actual_index]
        prefix = ">" if actual_index == index else " "
        label = "{} {}".format(prefix, filename[:-3])
        y = title_y + line_height * (i + 1)
        ev3.screen.draw_text(0, y, label)


while True:
    index = 0
    scroll_offset = 0
    draw_menu(index, scroll_offset)

    # Navigation loop
    while True:
        pressed = ev3.buttons.pressed()

        if Button.UP in pressed:
            index = (index - 1) % len(files)
            if index < scroll_offset:
                scroll_offset = index
            draw_menu(index, scroll_offset)
            time.sleep(0.2)

        elif Button.DOWN in pressed:
            index = (index + 1) % len(files)
            if index >= scroll_offset + MAX_VISIBLE:
                scroll_offset = index - MAX_VISIBLE + 1
            draw_menu(index, scroll_offset)
            time.sleep(0.2)

        elif Button.CENTER in pressed:
            folder, filename = files[index]
            ev3.screen.clear()
            ev3.screen.print("Running:")
            ev3.screen.print(filename)
            time.sleep(1)
            break

    # Run selected file
    folder, filename = files[index]
    selected_path = "{}/{}".format(folder, filename)

    try:
        with open(selected_path) as f:
            code = f.read()

        exec(code)
        time.sleep(1)

    except SystemExit:
        pass  # Exit cleanly from inside script

    except Exception as e:
        ev3.screen.clear()
        ev3.screen.print("Error running:")
        ev3.screen.print(filename)
        ev3.screen.print(str(e))
        time.sleep(2)