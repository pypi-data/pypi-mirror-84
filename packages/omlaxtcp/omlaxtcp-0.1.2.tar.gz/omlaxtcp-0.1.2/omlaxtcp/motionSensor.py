import RPi.GPIO as GPIO
# Allows for the implementation of the onboard RPi GPIO pins.
import time
# Used to generate delay.
import TCP
# Allows for the transmission of relevant messages via TCP.
import tempSensor

global buzzerPin
buzzerPin = 4
# Default GPIO pin for buzzer


def setup(motion):
    """
    Configures motion sensor for input in accordance to the GPIO pin provided.

    Parameters:
    motion(int): Motion sensor pin
    """
    GPIO.setmode(GPIO.BCM)
    # Sets pin numbering system
    GPIO.setup(motion, GPIO.IN)
    # Configures given pin for input usage.


def motion_detect(motion):
    """
    Determines if an individual triggers a motion sensor.

    Parameters:
    motion(int): Second motion sensor pin
    """
    if (GPIO.input(motion) == 1):
        print "Motion detected"
    else:
        print "No motion detected"


def direc_detect(motion_out, motion_in):
    """
    Determines the direction in which an individual is travelling,
    by assessing the sequence of triggers between two motion sensors.

    Parameters:
    motion_out(int): Outside motion sensor pin
    motion_in(int): Inside motion sensor pin
    """
    if (GPIO.input(motion_out) == 1):
        # Determines if outside motion sensor is triggered first.
        init_trig(motion_in)
        # Wait atleast 4 seconds for the corresponding sensor to trigger.
        ensure_low(motion_out, motion_in)
        # Ensure that both motion sensors are low/are not triggered.

    if (GPIO.input(motion_in) == 1):
        # Determines if inside motion sensor is triggered first.
        init_trig(motion_out)
        # Wait atleast 4 seconds for the corresponding sensor to trigger.
        ensure_low(motion_out, motion_in)
        # Ensure that both motion sensors are low/are not triggered.

def direc_detect_with_BuzzandTemp(motion_out, motion_in):
    """
    Determines the direction in which an individual is travelling,
    by assessing the sequence of triggers between two motion sensors.
    Includes buzzer and temperature sensor operation. 

    Parameters:
    motion_out(int): Outside motion sensor pin
    motion_in(int): Inside motion sensor pin
    """
    if (GPIO.input(motion_out) == 1):
        # Determines if outside motion sensor is triggered first.
        init_trig_with_BuzzandTemp(motion_in)
        # Wait atleast 4 seconds for the corresponding sensor to trigger.
        ensure_low(motion_out, motion_in)
        # Ensure that both motion sensors are low/are not triggered.

    if (GPIO.input(motion_in) == 1):
        # Determines if inside motion sensor is triggered first.
        init_trig(motion_out)
        # Wait atleast 4 seconds for the corresponding sensor to trigger.
        ensure_low_with_BuzzandTemp(motion_out, motion_in)
        # Ensure that both motion sensors are low/are not triggered.
        
def speed_detect(motion_first, motion_second, distance):
    """
    Determines the direction in which an individual is travelling,
    by assessing the time between the triggering of two motion sensors.

    Parameters:
    motion_out(int): Outside motion sensor pin
    motion_in(int): Inside motion sensor pin
    """
    if (GPIO.input(motion_first) == 1):
        # Determines if first motion sensor is triggered first.
        speed(timing(motion_second), distance)
        # Sends speed as message to server when corresponding sensor triggered.
        ensure_low(motion_first, motion_second)
        # Ensure that both motion sensors are low/are not triggered.

    if (GPIO.input(motion_second) == 1):
        # Determines if second motion sensor is triggered first.
        speed(timing(motion_first), distance)
        # Sends speed as message to server when corresponding sensor triggered.
        ensure_low(motion_first, motion_second)
        # Ensure that both motion sensors are low/are not triggered.


def init_trig_with_BuzzandTemp(motion):
    """
    Waits up to 4 seconds until corresponding sensor is triggered.
    If sensor triggered and temperature sensor not been triggered prior,
    buzzer will go off.
    If had triggered prior, direction of movement sent as message to server.

    Parameters:
    motion(int): Second motion sensor pin
    """
    for x in range(40):
        # Loop for 40 iterations.
        time.sleep(0.1)
        # Delay for 10ms.
        if (GPIO.input(motion) == 1):
            # Determines if corresponding motion sensor is triggered.
            if (motion == 1) and (!tempSensor.scanned):
                # Determines if user enters without temp scan.
                GPIO.setup(buzzerPin, GPIO.OUT)
                # Set buzzerPin to output mode.
                GPIO.output(buzzerPin, GPIO.HIGH)
                # Set buzzerPin high.
                time.sleep(2)
                # Delay for 2 seconds.
                GPIO.output(buzzerPin, GPIO.LOW)
                # Set buzzerPin low.
                print("BUZZ")
                break
            else:
                TCP.client(str(motion))
                # Sends direction of motion as message to the connected server.
                tempSensor.scanned = False
                break

def init_trig(motion):
    """
    Waits up to 4 seconds until corresponding sensor is triggered.
    motion(int): Second motion sensor pin
    """
    for x in range(40):
        # Loop for 40 iterations.
        time.sleep(0.1)
        # Delay for 10ms.
        if (GPIO.input(motion) == 1):
            # Determines if corresponding motion sensor is triggered.
                TCP.client(str(motion))
                # Sends direction of motion as message to the connected server.
                break

def timing(motion):
    """
    Returns calculated time between triggering of corresponding motion sensor
    after the first motion sensor is triggered. Accurate to 10ms.

    Parameters:
    motion(int): Second motion sensor pin

    Returns:
    tic - toc (float): Length of time in seconds
    """
    tic = time.perf_counter()
    # Establishes time in which first motion sensor is triggered.
    while (GPIO.input(motion) != 1):
        # Determines if corresponding motion sensor is triggered.
        time.sleep(0.01)
        # Delay by 10ms.

    toc = time.perf_counter()
    # Establishes time in which second motion sensor is triggered.
    return tic - toc


def speed(time, distance):
    """
    Calculates and sends speed as a message to server.

    Parameters:
    time(float): Time given in seconds
    distance(float): Distance given in meters
    """
    speed = distance/time
    # Calculates speed in meters/second.
    TCP.client(str(speed))
    # Sends speed as a message to the connected server.


def ensure_low(motion_out, motion_in):
    """
    Returns only when both motion sensors are low/are not triggered.

    Parameters:
    motion_out(int): Outside motion sensor pin
    motion_in(int): Inside motion sensor pin
    """
    while (GPIO.input(motion_out) == 1) or (GPIO.input(motion_in) == 1):
        # Determines if either of the two motion sensors are high/triggered.
        time.sleep(0.1)
        # Delay by 100ms.


def setBuzzerPin(Pin):
    """
    Sets the Buzzer GPIO Pin to desired Pin value

    Parameters:
    Pin(int): A pin number
    """
    global buzzerPin
    buzzerPin = Pin
    # Replaces old pin value with the new Pin argument.
