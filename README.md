Rpi Home Automation
======

Introduction
------------

Rpi Home Automation is a complete setup to automate your home via Raspberry Pi 3 B/B+.<br/><br/>
The setup includes:
- rpi server (a script that handles messages sent from the app to control client devices)
- App (app to control the Raspberry Pi 3 B/B+ (rpi) )
- a generic python script for a wlan-client-device (this script can be adjusted to fulfill the desired needs of the client device)

Devices can be controlled via rf (433MHz) and/or WLAN.
In order to control a device through rf, a RF 433MHz module is needed (See: Wiring diagramm)

Controlled devices can be:<br/><br/>
**rf:**
- generic low-cost GPIO RF 433MHz modules
- generic RF 433 MHz outlets
- rf relais 433MHz
- any other 433 MHz devices that lets you pick out or set the transmitted code

**wlan:**
- another Raspberry Pi 3 B/B+
- Pi zero
- esp8266
- any other programmable device connected to the same network

The current state is not usable yet, as it is still under development – so is the README not complete!

Supported hardware
------------
**rf:**
- Most generic 433MHz capable modules connected via GPIO to a Raspberry Pi. (cost: ~2€)

<img src="readme/433MHzRF.png" width="30%" height="30%">

Compatibility
------------
**rf:**
- Generic 433MHz outlets. (cost: ~ 15€/3pcs)

<img src="readme/433MHzoutlet.png" width="30%" height="30%">

Installation (Incomplete)
------------

**Raspberry Pi 3:**

-   Install *Raspbian OS* on your Raspberry Pi 3
-   Connect your Raspberry Pi 3 with your home network via WLAN
-   Copy the folder *rpi\_server* to your Raspberry Pi 3.
-   Turn off your Raspberry Pi 3 and connect the 433MHz RF-Module with your Raspberry Pi 3 (See: Wiring diagram)
-   Turn on your Raspberry Pi 3 and run *rpi\_server.py*

<img src="readme/rpi_setup.png" width="120%" height="120%">

**Remote outlets:**

Each remote outlet can be configured through dip switches. These have to be unique in order to identify them.

<img src="readme/dipswitch.png" width="30%" height="30%">

Each switch can have two states: *Up* and *Down*.

*Up* means *On* (1) and *Down* means *Off* (0)

The first five switches (1 - 5) represent the unique code and the switches A to E are the name.

Switches 1 to 5 can be set individually to set a unique code for this particular outlet. For the switches A to E can only one switch be set. Eg. if A is *On,* then B to C have to be *Off*.

So in the example below, dip switch 1 and 3 are *On* and switch A is also *On*.

Because A is *On*, B to E have to be *Off*.

<img src="readme/dipswitch_example.png" width="30%" height="30%">

As *On* means 1 and *Off* means 0, the above example would translate to:
```
-   10100 for the switches 1 to 5 and
-   10000 for switch A to E.
```
So the unique code for this outlet would be:
```
10100 10000
```

Wiring Diagram:
---------------

<img src="readme/rpi_rf_wiring.png" width="40%" height="40%">

```
TX:
   GND > GND
   VCC > 5V
  DATA > PIN 11 (GPIO17)

RX:
   VCC > 5V
   GND > GND
   DATA > PIN 13 (GPIO27)
```

Configure Android App
---------------------
```
comming soon
```

License
---------------
This project is released under:
```
Creative Commons Attribution-NonCommercial 4.0 International Public License
```
Summary: 
```
Can:
 - Distribute 
 - Modify
 
Cannot:
 - Commercial Use 
 - Sublicense
 
Must:
 - Give Credit 
 - Include Copyright 
 - State Changes
 ```
 View [LICENSE](LICENSE) for more infos.
