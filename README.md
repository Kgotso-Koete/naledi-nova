# Naledi Nova Telescope Navigator

This is my implementation of the **Raspberry Pi Planet Finder** project originally created by [Snowbiscuit](https://www.instructables.com/member/snowbiscuit/). This project creates a DIY digital navigation tool for stargazing, allowing you to automatically orient a telescope toward a chosen planet using real-time data and stepper motors.

- Naledi means "star" in SeSotho.

## Important Note

The planet finder can only find objects catalogued in the JPL Horizons [on-line solar system data](https://ssd.jpl.nasa.gov/horizons/app.html#/) and ephemeris computation service. So this can only find objects in the Solar System. Deep sky objects are not included.

---

## Demo

[Link to Demo](?)

---

## Screenshot

_Include a screenshot of your project in action, e.g., displaying planet data on the LCD screen or the telescope pointing to a planet._

## Project Overview

This project is a DIY tool for amateur astronomers, designed to make finding planets in the night sky easier. It automates the process of aligning a telescope with a selected planet using data from NASA’s JPL Horizons API, which provides real-time ephemeris data for celestial objects.

### Key Features

1. **User Input**: Use buttons to select different planets from a list.
2. **Data Retrieval**: Get up-to-date azimuth and elevation angles for each planet from JPL Horizons.
3. **Motorized Movement**: Stepper motors adjust the telescope’s azimuth (horizontal) and elevation (vertical) angles to point at the selected planet.
4. **User Feedback**: The 16x2 LCD displays the currently selected planet and its position data for easy navigation.

---

## What This Code Base Covers

This Python code runs on the Raspberry Pi to handle:

1. **Initialization**: Configures GPIO pins for motors and buttons, sets up the LCD, and prepares stepper motors for movement.
2. **Event Handlers**: Responds to button presses to select planets, align the telescope, or adjust settings.
3. **Data Fetching**: Uses Astroquery to access JPL Horizons data and fetch azimuth/elevation coordinates of planets.
4. **Motor Control**: Provides functions to move the telescope using stepper motors, with specific sequences for accurate positioning.
5. **LCD Display**: Shows the current planet selection and position coordinates, providing feedback for navigation.

---

## Bill of Materials

Here are the hardware components and tools required to build this project, following the exact parts as recommended in the original [Raspberry Pi Planet Finder tutorial](https://www.instructables.com/Raspberry-Pi-Planet-Finder/):

### Hardware Components

1. **Telescope**: Zhumell Z114 - 114 mm (4.5 inch) Tabletop Dobsonian
2. **Single-board Computer (SBC)**: Raspberry Pi 3B
3. **LCD Display**: 16x2 I2C LCD Display, preferably with a PCF8574 I2C expander (Model: YwRobot 1602)
4. **Stepper Motors**:
   - 28BYJ-48 5V Stepper Motors (x2, one for each axis)
   - ULN2003 Stepper Motor Driver Boards (x2, one for each motor)
5. **Buttons**: 3x Tactile push buttons (for select, increment, and decrement functions)
6. **Breadboard and Jumper Wires**: To connect components to the Raspberry Pi GPIO
7. **Power Supply**: Reliable 5V power supply, preferably with a capacity to handle the Raspberry Pi and both motors simultaneously

### Tools

1. **Screwdrivers**: For assembly and adjustment
2. **Soldering Kit**: For any necessary soldering (depending on motor connections)
3. **Multimeter**: For testing connections and voltage if needed

---

## Technology Stack

- **Programming Language**: Python 3.7.3
- **Libraries**:
  - **astroquery==0.4.7**: To fetch astronomical data from JPL Horizons API
  - **RPi.GPIO==0.7.0**: For controlling GPIO pins on the Raspberry Pi
  - **RPLCD==1.3.1**: To control the 16x2 LCD screen
  
- **Additional Software**:
  - **I2C Configuration**: Ensure I2C is enabled on the Raspberry Pi for LCD communication

- **Raspberry Pi operating system version**: 
    OS info based on command `cat /etc/os-release`
    
	PRETTY_NAME="Raspbian GNU/Linux 10 (buster)"
	NAME="Raspbian GNU/Linux"
	VERSION_ID="10"
	VERSION="10 (buster)"
	VERSION_CODENAME=buster
	ID=raspbian
	ID_LIKE=debian
	HOME_URL="http://www.raspbian.org/"
	SUPPORT_URL="http://www.raspbian.org/RaspbianForums"
	BUG_REPORT_URL="http://www.raspbian.org/RaspbianBugs"
     
    OS bit info based on command `getconf LONG_BIT`
	32

    OS cpu info based on command `uname -m`
	armv7l

---

## Tutorial Used

The project was inspired by [Raspberry Pi Planet Finder](https://www.instructables.com/Raspberry-Pi-Planet-Finder/) on Instructables. This tutorial is a comprehensive guide on building a sky navigation system for telescopes, especially useful for hobbyist astronomers.

---

## How to Build

### 1. Hardware Setup

- Connect the 16x2 I2C LCD display to the Raspberry Pi via I2C.
- Attach the 28BYJ-48 stepper motors to control azimuth and elevation angles of the telescope.
- Connect tactile buttons to the Raspberry Pi GPIO pins to handle user inputs.

### 2. Software Setup

1. Enable I2C on the Raspberry Pi: Run sudo raspi-config and enable I2C under "Interface Options."
2. Clone the Repository: Download this project to your Raspberry Pi.
3. Install [Python 3.7.3](https://www.python.org/downloads/release/python-372/).
4. Clone this repository: `git clone ??`.
5. `cd` into `naledi-nova`: `cd naledi-nova`.
6. Install [virtualenv](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/#installing-virtualenv).
7. Create a new virtualenv called "env-naledi-nova": `python3 -m venv env-naledi-nova`.
8. Set the local virtualenv to "env-naledi-nova
": `source env-naledi-nova/bin/activate`.
   If all went well then your command line prompt should now start with `(env-naledi-nova)`. To deactivate navigate to the project directory and run the command `deactivate`
9. Install the required packages: `pip3 install -r requirements.txt`
10.Set up a background worker: 
   run `crontab -e` 
   add the line`@reboot /home/kgotso-koete/Documents/Projects/naledi-nova/env-naledi-nova/bin/python /home/kgotso-koete/Documents/Projects/naledi-nova/naledi-nova.py`


### 3. Running the Code

---

- Execute the script 'python3 planet_finder.py' to test the code
- Set up a background process (cron job) using instructions in the tutorial

---

### Acknowledgements

Special thanks to Snowbiscuit for creating a really cool astronomy project [tutorial](https://www.instructables.com/Raspberry-Pi-Planet-Finder/). I got to explore both astronomy and my Raspberry Pi with this experiment.

---

### License

The codebase is MIT licensed unless otherwise specified.

---

To be modified further by Kgotso Koete
<br/>
Johannesburg, South Africa
