import serial

def SetupConnection():
    # Opens a serialport
    global ser
    ser = serial.Serial()

    # Sets baudrate to 19200
    ser.baudrate = 19200

    # Sets the port
    ser.port = "COM3"
    return(ser)

#Returns a list with all connected ports.
def getPorts():
    ports = list(serial.tools.list_ports.comports())
    return(ports)