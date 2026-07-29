#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, InfraredSensor
from pybricks.parameters import Port, Button, Color
from pybricks.tools import wait

import json
import socket

leverTypes = ("Reverser", "ThrottleAndBrake", "Throttle", "DynamicBrake", "TrainBrake", "LocoBrake")
brick = EV3Brick()

with open("assets/specs.json", "r") as f:
    specs = json.load(f)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((specs.get("HOST"), specs.get("PORT")))

sock.send((json.dumps({
    "type": "CONFIG",
    "left": "Reverser",
    "middle": None,
    "right": None,
    "color": None
}) + "\n").encode())

value = 0.0
selected = 0

while True:
    if Button.CENTER in brick.buttons.pressed():
        sock.send((json.dumps({
            "type": "END",
        }) + "\n").encode())
        sock.close()
        break

    if Button.UP in brick.buttons.pressed() and value < 100:
        value += 0.5

    if Button.DOWN in brick.buttons.pressed() and value > -100:
        value -= 0.5

    if Button.LEFT in brick.buttons.pressed() and selected > 0:
        selected -= 1
        sock.send((json.dumps({"type": "CONFIG", "left": leverTypes[selected], "middle": None, "right": None, "color": None}) + "\n").encode())

    if Button.RIGHT in brick.buttons.pressed() and selected < len(leverTypes) - 1:
        selected += 1
        sock.send((json.dumps({"type": "CONFIG", "left": leverTypes[selected], "middle": None, "right": None, "color": None}) + "\n").encode())

    brick.screen.clear()
    brick.screen.print("Selected:\n " + str(leverTypes[selected]))
    brick.screen.print("Value:\n " + str(value))

    sock.send((json.dumps({
        "type": "DATA",
        "left": value,
        "middle": None,
        "right": None,
        "color": None,
        "buttons": []
    }) + "\n").encode())

    wait(100)