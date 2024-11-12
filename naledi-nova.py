# Import the CharLCD class from the RPLCD.i2c module to interact with an LCD screen via I2C.
from RPLCD.i2c import CharLCD
# Import time module to use sleep functions for delays.
import time
# Import GPIO library to control the Raspberry Pi’s GPIO pins.
import RPi.GPIO as GPIO
# Import the Horizons class from astroquery.jplhorizons to get astronomical data.
from astroquery.jplhorizons import Horizons

# Define the observatory location code ('078' for an observatory near the user).
nearestObservatory = '078' # Johannesburg
# Variable to keep track of whether the device is in setup mode.
inSetUp = True
# Index to track the selected planet.
planetIndex = 0
# Define the GPIO pins for the azimuth (horizontal) stepper motor.
stepperPinsAZ = [7,11,13,15]
# Define the GPIO pins for the elevation (vertical) stepper motor.
stepperPinsEL = [40, 38, 36, 32]
# Define the GPIO pin for the "select" button.
selectBtnPin = 33
# Define the GPIO pin for the "increase" button.
incBtnPin = 37
# Define the GPIO pin for the "decrease" button.
decBtnPin = 35
# Define the identifier for Mars as 499 (used later for testing).
mars = 499
# List of planetary body IDs to select from (e.g., 199 for Mercury, 299 for Venus, etc.).
planets = [199, 299, 301, 499, 599, 699, 799, 899, 999]
# Names of the planets matching the IDs in the planets list.
planetNames = ["Mercury", "Venus", "Moon", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
# time that the finder should pause to give the user a chance to Observe
finderObservationPause = 30

# Callback function for the "select" button. This executes when the "select" button is pressed.
def okSelect(channel):
	global planetIndex
	global planets
	global planetNames
	global stepperPinsAZ
	global stepperPinsEL

	 # Check if the button is pressed.
	if GPIO.input(channel) == GPIO.LOW:
		eph = getPlanetInfo(planets[planetIndex]) # Get the selected planet's info.
		percentageArcAZ = (eph['AZ'][0]) / 360  # Convert azimuth angle to percentage.
		percentageArcEL = (eph['EL'][0]) / 360 # Convert elevation angle to percentage.
		stepsNeededAZ = int(percentageArcAZ * 512) # Calculate required steps for azimuth, 512 steps is 360degrees.
		stepsNeededEL = int(percentageArcEL * 512) # Calculate required steps for azimuth, 512 steps is 360degrees.

		lcd.clear() # Clear the LCD display.
		lcd.write_string(planetNames[planetIndex]) # Display the planet's name.
		lcd.crlf() # Move to the next line.
		lcd.write_string("AZ " + str(int(eph['AZ'][0])) + " EL " + str(int(eph['EL'][0]))) # Display angles.
		time.sleep(1)
		print("ok button pressed")  # Log button press to console.

		# Move the azimuth motor.
		if stepsNeededAZ > 256:
			moveStepperBack(stepperPinsAZ, (512-stepsNeededAZ)) # Rotate counterclockwise.
		else:
			moveStepper(stepperPinsAZ, stepsNeededAZ)  # Rotate clockwise.
		time.sleep(1)

		# Move the elevation motor.
		if stepsNeededEL < 0:
			moveStepperBack(stepperPinsEL, -stepsNeededEL) #rotates downwards
		else:
			moveStepper(stepperPinsEL, stepsNeededEL) #rotates upwards
        
		# give the user time to observe before returning to the original position   
		time.sleep(finderObservationPause)

		# Return elevation motor to starting position.
		if stepsNeededEL < 0:
			moveStepper(stepperPinsEL, -stepsNeededEL)
		else:
			moveStepperBack(stepperPinsEL, stepsNeededEL)
		time.sleep(1)

		# Return azimuth motor to starting position.
		if stepsNeededAZ > 256:
			moveStepper(stepperPinsAZ, (512-stepsNeededAZ)) #rotates anticlockwise
		else:
			moveStepperBack(stepperPinsAZ, stepsNeededAZ) #rotates clockwise
		time.sleep(1)
		lcd.clear()
		lcd.write_string(planetNames[planetIndex])

# Function for the "increase" button to increment the planet index.
def incSelect(channel):
	global planetIndex
	global planetNames
	if GPIO.input(channel) == GPIO.LOW:
		if planetIndex < 8: # Check bounds to avoid index error.
			planetIndex = planetIndex + 1 # Move to the next planet.
		lcd.clear()
		lcd.write_string(planetNames[planetIndex]) # Display the updated planet name.
		print("inc button pressed") # Log button press.
		time.sleep(1)

# Function for the "decrease" button to decrement the planet index.
def decSelect(channel):
	global planetIndex
	global planetNames
	if GPIO.input(channel) == GPIO.LOW:
		if planetIndex > 0: # Check bounds to avoid index error.
			planetIndex = planetIndex - 1  # Move to the previous planet.
		lcd.clear()
		lcd.write_string(planetNames[planetIndex]) # Display the updated planet name.
		print("dec button pressed")  # Log button press.
		time.sleep(1)

# Function to start the setup process.
def startUp():
	lcd.clear()
	lcd.write_string("Setup Mode:")
	lcd.crlf()
	lcd.write_string("Adjust Vertical")
	# Set up button event listeners for setup mode.
	GPIO.add_event_detect(selectBtnPin, GPIO.FALLING, callback=startUpNext, bouncetime=200)
	GPIO.add_event_detect(incBtnPin, GPIO.FALLING, callback=increaseEL, bouncetime=200)
	GPIO.add_event_detect(decBtnPin, GPIO.FALLING, callback=decreaseEL, bouncetime=200)
	time.sleep(1)

# Rotate azimuth motor clockwise.
def increaseAZ(channel):
	if GPIO.input(channel) == GPIO.LOW:
		moveStepper(stepperPinsAZ, 32)

# Rotate azimuth motor counterclockwise.
def decreaseAZ(channel):
	if GPIO.input(channel) == GPIO.LOW:
		moveStepperBack(stepperPinsAZ, 32)

# Rotate elevation motor upwards.
def increaseEL(channel):
	if GPIO.input(channel) == GPIO.LOW:
		moveStepper(stepperPinsEL, 32)

# Rotate elevation motor downwards.
def decreaseEL(channel):
	if GPIO.input(channel) == GPIO.LOW:
		moveStepperBack(stepperPinsEL, 32)

# Continue the setup process to adjust rotation.
def startUpNext(channel):
	if GPIO.input(channel) == GPIO.LOW:
		lcd.clear
		lcd.write_string(" Setup Mode:")
		lcd.crlf()
		lcd.write_string("Adjust  Rotation")

		# Reassign button event listeners for rotation adjustment.
		GPIO.remove_event_detect(selectBtnPin)
		GPIO.remove_event_detect(incBtnPin)
		GPIO.remove_event_detect(decBtnPin)
		GPIO.add_event_detect(selectBtnPin, GPIO.FALLING, callback=startUpFinish, bouncetime=200)
		GPIO.add_event_detect(incBtnPin, GPIO.FALLING, callback=increaseAZ, bouncetime=200)
		GPIO.add_event_detect(decBtnPin, GPIO.FALLING, callback=decreaseAZ, bouncetime=200)
		time.sleep(1)

# Finalize the setup process.
def startUpFinish(channel):
	if GPIO.input(channel) == GPIO.LOW:
		global inSetUp

		# Reassign button event listeners to normal mode functions.
		GPIO.remove_event_detect(selectBtnPin)
		GPIO.remove_event_detect(incBtnPin)
		GPIO.remove_event_detect(decBtnPin)
		GPIO.add_event_detect(selectBtnPin, GPIO.FALLING, callback=okSelect, bouncetime=500)#Setup event on falling edge
		GPIO.add_event_detect(incBtnPin, GPIO.FALLING, callback=incSelect, bouncetime=500)
		GPIO.add_event_detect(decBtnPin, GPIO.FALLING, callback=decSelect, bouncetime=500)
		inSetUp = False # Exit setup mode.
		time.sleep(1)

# Get planetary position data from Horizons.
def getPlanetInfo(planet):
	obj = Horizons(id=planet, location=nearestObservatory, epochs=None, id_type='majorbody')
	eph = obj.ephemerides()
	return eph


"""
Stepper Motor Basics
Stepper motors move in small, precise increments (steps), making them ideal for applications requiring 
accurate positioning, like pointing a telescope. The motor in this project, a 28BYJ-48 stepper motor, 
has four coils (or phases) that are energized in a specific sequence to create the rotation.


Half-Step Sequence Array (halfstep_seq)
The halfstep_seq array defines the sequence in which the motor’s coils should be energized to achieve half-stepping. 
Half-stepping is a driving method where the motor takes finer steps, effectively doubling the resolution and increasing precision, 
which is particularly helpful in astronomy for precise alignment.

Each sub-array represents a specific pattern of on/off states for the four coils, corresponding to one half-step. In each half-step:

1 means the coil is energized.
0 means the coil is off.
For example, [1, 0, 0, 0] means only the first coil is energized, [1, 1, 0, 0] means the first two coils are energized, and so on. 
By energizing the coils in the order specified by halfstep_seq, the motor rotates in a controlled, predictable way.

How Half-Stepping Works
In each step of the loop, the moveStepper function:
	Iterates through each sub-array in halfstep_seq, energizing coils according to that sub-array.
	Energizes the coils in the sequence specified, creating a smooth rotation.
	After going through the entire sequence, the motor completes a single half-step.
Since this motor has 512 half-steps per full rotation, you need to call moveStepper with stepsNeeded equal 
to 512 to make it turn 360° (one full rotation).


The Loop Structure in moveStepper
Outer Loop (for i in range(stepsNeeded)): 
	Repeats the full sequence for the required number of steps (stepsNeeded), which determines how far the motor should turn.
Half-Step Loop (for halfstep in range(8)): 
	Cycles through each sub-array in halfstep_seq, setting the output state for each half-step.
Pin Loop (for pin in range(4)): 
	Sets each GPIO pin (axis[pin]) on or off according to the halfstep_seq array, which controls the four motor coils.

time.sleep(0.002): Adds a delay between half-steps, controlling the motor’s speed. Adjusting this delay changes the motor’s rotation speed, but a very short delay may lead to issues if the motor is too fast to respond accurately.

"""

# Move a stepper motor forward by a specified number of steps.
def moveStepper(axis, stepsNeeded):
	halfstep_seq = [
		[1,0,0,0],
		[1,1,0,0],
		[0,1,0,0],
		[0,1,1,0],
		[0,0,1,0],
		[0,0,1,1],
		[0,0,0,1],
		[1,0,0,1]
	]
	for i in range(stepsNeeded):
		for halfstep in range(8):
			for pin in range(4):
				GPIO.output(axis[pin], halfstep_seq[halfstep][pin])
			time.sleep(0.002)

def moveStepperBack(axis, stepsNeeded):
	halfstep_seq = [
		[1,0,0,1],
		[0,0,0,1],
		[0,0,1,1],
		[0,0,1,0],
		[0,1,1,0],
		[0,1,0,0],
		[1,1,0,0],
		[1,0,0,0]
	]
	for i in range(stepsNeeded):
		for halfstep in range(8):
			for pin in range(4):
				GPIO.output(axis[pin], halfstep_seq[halfstep][pin])
			time.sleep(0.002)


GPIO.setmode(GPIO.BOARD)

for pin in stepperPinsAZ + stepperPinsEL:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin,0)


lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True,
              backlight_enabled=True)
lcd.clear()

GPIO.setup(selectBtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(incBtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(decBtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

startUp()

while inSetUp:
	time.sleep(1)

lcd.clear()
lcd.write_string("Welcome to")
lcd.crlf()
lcd.write_string("Naledi Nova -> *")
time.sleep(2)

lcd.clear()
lcd.write_string("Select a planet")
lcd.crlf()
lcd.write_string("Mercury")
time.sleep(2)

while True:
	time.sleep(1)
