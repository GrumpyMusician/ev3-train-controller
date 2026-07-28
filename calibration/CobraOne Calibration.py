#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, InfraredSensor
from pybricks.parameters import Port, Button, Color
from pybricks.tools import wait

import json
import socket

brick = EV3Brick()
leftLever = Motor(Port.A)
middleLever = Motor(Port.B)
rightLever = Motor(Port.C)
color = ColorSensor(Port.S2)
touch = TouchSensor(Port.S3)
beacon = InfraredSensor(Port.S4)

with open("assets/specs.json", "r") as f:
    specs = json.load(f)
leftLeverMAX = specs.get("left")
middleLeverMAX = specs.get("middle")
rightLeverMAX = specs.get("right")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((specs.get("HOST"), specs.get("PORT")))

# Unified button map (channel: {button: (sequence)})
buttons = {
    -1: {},
    0: {},
    1: {}, 
    2: {}, 
    3: {}, 
    4: {}  
}

sock.send((json.dumps({
    "type": "CONFIG",
    "left": "Reverser",
    "middle": "ThrottleAndBrake",
    "right": "Throttle",
    "color": None
}) + "\n").encode())
brick.screen.print("Left: Reverser\nMiddle: Throt & Brk\nRight: Throttle\nTouch sensor\nto proceed")

# Get current buttons per channel
def get_buttons(channel):
    if channel == -1:
        return ["touch"] if touch.pressed() else []
    elif channel == 0:
        return brick.buttons.pressed()
    else:
        return beacon.buttons(channel)

def handle_buttons(mapping, index_map, prev_map):
    output = []

    for ch in mapping:
        current = get_buttons(ch)

        for btn, sequence in mapping[ch].items():
            is_pressed = btn in current
            was_pressed = prev_map[ch][btn]

            # Output current sequence while button is held
            if is_pressed:
                key = sequence[index_map[ch][btn]]
                output.append(key)

            # Advance sequence only after full release + next press (falling edge then rising edge)
            if was_pressed and not is_pressed and len(sequence) > 1:
                index_map[ch][btn] = (index_map[ch][btn] + 1) % len(sequence)

            # Update previous press state
            prev_map[ch][btn] = is_pressed

    return output

# Normalize lever input
def scrunch(motor, max_val):
    if not max_val:
        return 0  # avoid division if config is missing or zero
    angle = motor.angle()
    s = (min(max(angle / max_val * 100, 0), 100) - 50) * 2
    return 0 if -5 < s < 5 else 95 + (s - 95) if s > 95 else -95 - (-95 - s) if s < -95 else s

# State trackers
sequence_index = {ch: {btn: 0 for btn in buttons[ch]} for ch in buttons}
prev_pressed = {ch: {btn: False for btn in buttons[ch]} for ch in buttons}

isConfigRotation = False
while True:
    if Button.CENTER in brick.buttons.pressed():
        sock.send((json.dumps({
            "type": "END",
        }) + "\n").encode())
        sock.close()
        break

    if isConfigRotation == False and touch.pressed():
        isConfigRotation = True
        brick.speaker.beep()
        sock.send((json.dumps({
            "type": "CONFIG",
            "left": "DynamicBrake",
            "middle": "TrainBrake",
            "right": "LocoBrake",
            "color": None
        }) + "\n").encode())
        brick.screen.print("Left: DynamicBrake\nMiddle: TrainBrake\nRight: LocoBrake\nTouch sensor\nto proceed")

    elif isConfigRotation == True and touch.pressed():
        isConfigRotation = False
        brick.speaker.beep()
        sock.send((json.dumps({
            "type": "CONFIG",
            "left": "Reverser",
            "middle": "ThrottleAndBrake",
            "right": "Throttle",
            "color": None
        }) + "\n").encode())
        brick.screen.print("Left: Reverser\nMiddle: Throt & Brk\nRight: Throttle\nTouch sensor\nto proceed")
    
    buttonsList = handle_buttons(buttons, sequence_index, prev_pressed)

    sock.send((json.dumps({
        "type": "DATA",
        "left": scrunch(leftLever, leftLeverMAX),
        "middle": scrunch(middleLever, middleLeverMAX),
        "right": scrunch(rightLever, rightLeverMAX),
        "color": None,
        "buttons": buttonsList
    }) + "\n").encode())

    wait(5)