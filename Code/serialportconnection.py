import serial
import serial.tools.list_ports

def SetupConnection(port, baudrate):
    # Opens a serialport
    global ser
    ser = serial.Serial()

    # Sets baudrate to 19200
    ser.baudrate = baudrate

    # Sets the port
    ser.port = port
    return(ser)

#Returns a list with all connected ports.
def getPorts():
    ports = list(serial.tools.list_ports.comports())
    return(ports)