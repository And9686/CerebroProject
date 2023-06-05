import serial

# Initialize Serial (conficuration)
def initSerial():
    global ser  # Serial Object
    ser = serial.Serial('COM4',    # The COM changes with differentn boards and PCs
                    baudrate=115200,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=12)
    print("Serial port initialized!")

# Close Serial Connection with Arduino
def closeSerial():
    if 'ser' in globals():
        ser.close()
        print("Serial port closed!")
    else:
        print("Serial port never started!")

def sendMessage(message):
    ser.write(message.encode())
    print("Message sent!")

def readMessage():
    message = ser.read(100) 
    print("Message read!")
    return message.decode()