import pigpio
import smbus2
import time
import crcmod.predefined
import TCP

global scanned, init
scanned = False
init = False


def setup(channel, omAddress, arraysize):
    """
    Enables I2C communication between Raspberry Pi and the temperature sensor.

    Parameters:
    channel(int): Raspberry Pi i2c channel
    omAddress(int): Omron I2C address
    arraysize(int): Size of thermal array
    """
    global BUFFER_LENGTH
    global tdata_raw
    global handle
    global tdata
    global pi
    BUFFER_LENGTH = (arraysize*2) + 3
    # Establish data buffer size.
    pi = pigpio.pi()
    bus = smbus2.SMBus(channel)
    # Create a bus for I2C communication.
    time.sleep(0.1)
    # Delay for 10ms.
    handle = pi.i2c_open(channel, omAddress)
    tdata_raw = [0]*BUFFER_LENGTH
    tdata = [0.0]*arraysize


def feverScanner(maxtemp):
    """
    Determines if an individual is standing infront of the temperature sensor,
    waits a full second and reads the temperature value again to gain a more
    stable value. Also determines if temperature is above that of the norm.
    This data is relayed as a message to the server.
    """
    global init
    global scanned
    tempReading()
    if (tdata[0] > roomtemp) and (tdata[0] > 30):
        if (!init):
            init = True
            feverScanner()
        else:
            init = False
            scanned = True
            TCP.client(str(tdata[0]))
            if (tdata[0]) > maxtemp:
                scanned = False
                time.sleep(1)


def tempReading():
    """
    Determines the temperature of an object in front of the temperature sensor.
    """
    global tdata
    time.sleep(1)
    (bytes_read, tdata_raw) = pi.i2c_read_device(handle, BUFFER_LENGTH)
    # Reads raw data and number of bytes read
    a = 0
    b = len(tdata_raw)-2
    for i in range(2, b, 2):
        # Converts raw data to detected individual temperature in degrees celsius.
        # Starts at second byte as first byte is used for room temperature.
        tdata[a] = float((tdata_raw[i+1] << 8) | tdata_raw[i])/10
        a += 1


def roomtemp():
    """
    Determines the room temperature.
    """
    global roomtemp
    tPAT = float((tdata_raw[1] << 8) | tdata_raw[0])/10
    # Converts raw data to room temperature in degrees celsius.
    # First byte of raw data represents room temperature.
    roomtemp = tPAT


def getroomtempValue():
    """
    Retreives the most recently determined room temperature reading.

    Returns:
    roomtemp(float): Room temperature in degrees celsius
    """
    return(roomtemp)


def gettempReadingValue():
    """
    Retreives the most recently determined temperature reading.

    Returns:
    tdata[0](float): Temperature in degrees celsius
    """
    return(tdata[0])
