## Hi there 👋

Mindstorms for Train Simulators is a system of devices that utilizes Lego Mindstorms EV3 bricks to control cab systems for Train Simulator Classic and World of Subways, and I plan on implementing this for Train Simulator World!

## Get Involved 🪄

Lego Mindstorms was discontinued in 2022, meaning that, although there are still a lot of systems still running, this system can be ported to newer Spike PRIME kits, if anyone is interested in joining.  
There is also a possibility of using Raspberry Pi HATS that utilizes the newer LPF2 ports, doing away with the technic hubs.  
Unfortunately, I do not have the money in buying the Spike PRIME kit.

<img width="1080" height="498" alt="image" src="https://github.com/user-attachments/assets/0bf60830-60ff-4851-a32b-0f9aec39dd1e" />


## How to Use 💻

> :warning: **WiFi Issue**: Unfortunately, the connection between the EV3 brick and the computer may result in the temporary loss of WiFi. There's not much I can do here. Luckily, you are driving an offline train that doesn't need WiFi. But this means that you can't play the game while watching a Youtube video. Not like you should do that anyways.  

This project requires:
* Lego Mindstorms EV3 Brick, with three motors, a color sensor, a touch sensor, an infared sensor, and a infared beacon... all parts are from this [kit](https://www.lego.com/en-us/product/lego-mindstorms-ev3-31313)
* Raspberry Pi
* Computer running the Train Simulator

### Setting up the EV3 Brick 🧱:

> This is the hardest part of the setup process! (You will also have to assemble your lego machine before this).

* Although the EV3 brick doesn't take much processing power, it is power hungry. It is recommended that you use the EV3 brick with a Battery Pack, rechargable AA batteries, or [Battery Eliminator Kit](https://www.batteryeliminatorkits.com/product-p/6aa-eliminator-kit.htm) rated for 6 AA batteries with no more than 9 volts and 2 amps, but no less than 7 volts, rated for inside use only. You might burn through a significant number of traditional AA batteries otherwise.
* The EV3 brick utilizes Micropython. Please follow installation instructions [here](https://education.lego.com/en-us/product-resources/mindstorms-ev3/teacher-resources/python-for-ev3/) needed to install the operating system, as well as installing VSCode and the necessary [Micropython extension](https://marketplace.visualstudio.com/items?itemName=lego-education.ev3-micropython) to connect to the EV3 brick. Transfer the files from the [EV3CabControl Repository](https://github.com/Mindstorms-for-Train-Simulators/EV3CabControl) into the EV3 Brick.
 * It is not neccessary to have VSCode to run the software, only to install and add new rolling stock configurations! When not updating or installing, navigate to ``main.py`` in the EV3 brick and run the script.
* The system requires a plethora of motors and sensors. Three motors should be connected to port A, B, and C. Motor A will be the leftmost lever. Motor B will be the middle lever. Motor C will be rightmost lever. However, the roles of these motors will shift depending on the type of rolling stock, especially in trains that do not have such a braking system. The color sensor will need to be connected to port 2, touch sensor to port 3, and infared sensor to port 4. Because this is legos, you have the full freedom to choose where to put your devices, as long as they are connected to the correct port!
  * The color sensor must be able to read white, blue, green, yellow, red, black, and in that order from front to back. Please implement this as a sliding lever along the color sensor, and place it to the left of all three motors.
* This is modular, and new train configurations can be added within the programs folder, allowing you to selectively save whatever.
* If the motors does not match the values in the simulator, run "Callibration". It should be saved for future runs.
* **Connect to Computer:** Use the USB connecting cable to connect the EV3 brick to your computer. Ensure that your EV3 brick is in tethering mode by going to ``Wireless and Networks > Tethering`` and checking the ``Gadget`` option.
   * This is successful once an IP address is displayed on the top left of your EV3 brick.
   * You will need your computer's IP address (``192.168.X.XXX``) and to replace that in the ``/assets/specs.json`` file under the ``HOST`` key. You can obtain this by going to ``Network & Internet > [Your EV3 Ethernet]`` and looking for ``IPv4 Address: 192.168.X.XXX``.

### Setting up the Computer - Bridge 💻:
<!-- * Download all files from the [VirtualHID](https://github.com/Mindstorms-for-Train-Simulators/VirtualHID) repository.
* Install the latest Python program from the Microsoft Store. As of time of writing, it is [v3.13](https://apps.microsoft.com/detail/9PNRBTZXMB4Z?hl=en-us&gl=US&ocid=pdpshare).
* Open up Windows Command Prompt. Install the [keyboard](https://pypi.org/project/keyboard/) and [pyvjoy modules](https://pypi.org/project/pyvjoy/) with ``pip install keyboard pyvjoy``. If this doesn't work, try running Windows Command Prompt as an administrator. -->
* Install [vJoystick](https://sourceforge.net/projects/vjoystick/).
* Download the [VirtualHID](https://github.com/GrumpyMusician/VirtualHID/blob/main/dist/main.exe) program. It may give you a warning pop-up, but ignore it run the program anyways. It also prompt for connection permissions (this is necessary in order to listen to the EV3 brick), and it will launch a terminal to show you what the EV3 brick is sending, if at all. Feel free to ignore it!  
  <!--* Download the [VirtualHID](https://github.com/Mindstorms-for-Train-Simulators/VirtualHID) repository.-->

### Setting up the Computer - CobraOne Driver ♥️:
> ℹ️ World of Subways 3 and OpenBVE trains do not require drivers.
* CobraOne released two programs for [Train Simulator Classic](https://forums.dovetailgames.com/threads/ts-classic-raildriver-and-joystick-interface.72488/) and [Train Simulator World](https://forums.dovetailgames.com/threads/ts-world-raildriver-and-joystick-interface.61440/). Install the one(s) that you need. The setup procedure will be the same for both versions.
   <!--* If that doesn't work, you will have to set the levers manually with the python script. Open up the ``configs`` folder in the VirtualHID project and the executable for the programs you just downloaded (you can go split-screen). At the top of the program, go to ``Settings`` and then ``Assign Levers``. Work your way down from ``Reverser`` down to ``LocoBrake``. For each one, right click and press ``Assign Controller Axis``. Immediately press the appropiate ``.py`` file from the ``configs`` folder. Press ``OK`` and save when you are finished.-->
*   When setting up either CobraOne levers, use the CobraOne config program towards the bottom of the list that comes inside the brick. **Only run main.py!**
* * Jiggle the levers in order to configure the "assigned to" columns. The leftmost lever is X, middle Y, and rightmost Z. After pressing the touch sensor, the leftmost lever becomes RX, middle RY, rightmost RZ.
  * Reverser in both CobraOne applications must be set to X, ThrottleAndBrake Y, Throttle Z, DynamicBrake RX, TrainBrake RY, LocoBrake RZ. All other inputs can be left blank.
* The Lever config program can be used to set minimum and maximum values for your motors.
  
## To Do: 🗺️
Rolling Stock Configurations are found [here](https://docs.google.com/spreadsheets/d/1hxNL5QQfzBU_gq6_GBDmiY7Ld5c0j7snOmbEc2Otv3o/edit?ouid=100829421079514238916&usp=sheets_home&ths=true)! Future rolling stock will also be supplied on the spreadsheet as well.
