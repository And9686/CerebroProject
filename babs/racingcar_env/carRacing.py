import serial
import time
import gym
import numpy as np
import threading
import logging

threadState = True
inputData = None
a = [0]*3
a = np.array( [0.0, 0.0, 0.0] )  # Actions  (steer, gas, brake)
bool_do_not_quit = True  # Boolean to quit pyglet
pitch = 0
roll = 0

def init_serial():
    """Configures and stars the serial port between
     PC and Arduino"""
    global ser
    ser = serial.Serial('COM3',
                    baudrate=9600,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=12)

def closeSerial():
    """Closes the connection
        with the Arduino."""
    global ser
    if 'ser' in globals():
        ser.close()
        print("Porta Serie Fechada")
    else:
        print("Porta Serie Aberta")
# =================================================
def getValues():
    """ reads the values sent by the arduino to the PC
        --------------------
        returns an array with strings
    """
    
    global ser, status
    if status ==1:
        ser.write(b'a')
    elif status == 2:
        ser.write(b'i')
    
    raw = ser.readline()
    print("entrou")
    #raw = ser.read(ser.inWaiting())
    #print(raw)
    arduinoData = raw.decode('UTF-8')
    if status ==2:
        arduinoData = arduinoData.strip('\r\n').split(',')
    #print(arduinoData)
    return arduinoData


def writeValues(cmd):
    """ sends commands from PC
        to Arduino
        --------------------
        cmd has to be a string written with "", not ''
    """
    global ser
    ser.write(cmd)#.encode('utf-8')


#=============================================
def init_all():

    init_serial()
    time.sleep(2)
    setup()
#============================================
def setup():
    """guarantees syncronization between arduino program
    and game program. Sends command to calybrate the gyro"""

    global ser, status

    termCMD = input("Deseja iniciar o comando? Y/N")
    print(termCMD)
    while termCMD != 'Y':
        print(termCMD)
        termCMD = input("Deseja iniciar o comando? Y/N")
        break
    if termCMD == ('Y' or 'y'):
        print("Coloque o seu comando estatico, numa mesa..")
        status = 1
        aws = getValues()
        if aws == '1':
            print("gyro calibrated")
            status = 2


#=====================================================

def run_carRacing_wController(policy=None, record_video=False):
    """creates the enviroment for the car game
     -------------------------------------------
     receives a[0] - Steer, a[1] - Gas, a[2] - Brake
     """

    global bool_do_not_quit,a, restart
    env = gym.make('CarRacing-v0').env
    env.reset()
    env.render()
    while bool_do_not_quit:
        env.reset()
        restart = False
        t1 = time.time()  # Trial timer
        while bool_do_not_quit:
            controller_interpreter()
            print("VALORES DE A: Dir", a[0],"Acel", a[1],"trav", a[2])
            state, reward, done, info = env.step(a)
            #time.sleep(1/10)  # Slow down to 10fps
            if not record_video: # Faster, but you can as well call env.render() every time to play full window.
                env.render()
            if done or restart:
                t1 = time.time()-t1
                break
    env.close()
# ===============================================
def controller_interpreter():
    """ handles the arduino controller interpretation
    Processes the pitch and roll of the controller and
     outputs the corresponding value for array a
    -------------------------------------------
     outputs a[0] - Steer, a[1] - Gas, a[2] - Brake
    """

    global a, pitch, roll
    #Controls Gas and Brake
    if (pitch >-8 and pitch < 8):
        a[1] = 0
        a[2] = 0
    elif (pitch >= 8 and pitch< 15):
        a[1] += 0.0005
        a[2] = 0
    elif (pitch >= 15 and pitch< 40):
        a[1] += 0.005
        a[2] = 0
    elif (pitch >= 40):
        a[1] += 0.009
        a[2] = 0
    elif (pitch >= -8 and pitch < 0):
        a[1] = 0
        a[2] -= 0.0005
    elif (pitch >= -40 and pitch < -15):
        a[1] = 0
        a[2] -= 0.005
    elif (pitch < -40):
        a[1] = 0
        a[2] -= 0.009
    # Controls Direction
    if (roll >= -15 and roll <= 15):
        a[0] = 0
    elif (roll < -15):
        a[0] = -0.5
    elif (roll > 15):
        a[0] = +0.5
    #return a
#=============================================
def listenForData():
    """
    creates the thread responsible by the continuous reading of the arduino values
    """
    global threadState
    t_acq = threading.Thread(target=checkForData)
    t_acq.daemon = True
    t_acq.start()
# ==========================================
def updateData(myData):
    """
    converts the values read from arduino to float
    """
    global roll, pitch

    roll = float(myData[0])
    pitch = float(myData[1])
    print(roll,pitch)

#==================================================
def checkForData():
    """
    thread to continuously read the arduino values
    """

    global threadState

    logging.info("STARTING Acquisition thread")
    while threadState == True: # se a thread estiver ativada
        dataInput = getValues() #le a informacao do arduino
        updateData(dataInput) #atualiza a variavel da label
    logging.info("Stoping Acquisition Thread")

# ========
def main():
    global status, threadState, bool_do_not_quit
    init_serial()
    time.sleep(2)
    setup()
    #init_carRacing()
    print("Done!")
    status = 2
    listenForData()
    while ser.is_open:
        run_carRacing_wController()
    if (ser.is_open == False):
        threadState = False
        bool_do_not_quit = False
        time.sleep(3)

    """
    values = getValues()
    roll=float(values[0])
    pitch = float(values[1])
    """
# ========================================
main()
    
