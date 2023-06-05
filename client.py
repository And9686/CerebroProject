import json                                 # Data format trasmission package
import ssl                                  # Machine and server secure connection package
from websocket import create_connection     # Machine and server connection type package
import sys                                  # System tools package
from serial_connection import initSerial, closeSerial, sendMessage, readMessage

# Import authorization token
from auth import token, receivedData
import time

# Import cursor control functions
# import pyautogui


'''
TO-DO:
1. Multiple headsets code management
2. Select desired data subscription
'''


print("Setting up...")

# Check what devices are connected to EMOTIV Launcher
print("[] Checking headset connectivity...")

receivedData.send(json.dumps({
    "id": 1,
    "jsonrpc": "2.0",
    "method": "queryHeadsets",
    "params": {}
}))

detectedDevices = json.loads(receivedData.recv())["result"]

if len(detectedDevices) > 1:
    print("Multiple devices detected...\n",
          "Please select one to connect to:")
    # CONTINUAR ISTO

elif len(detectedDevices) == 1:
    print("Detected device: \"", detectedDevices[0]["customName"], "\" >", detectedDevices[0]["id"])
    deviceID = detectedDevices[0]["id"]
else:
    raise Exception("[Error C1] No device detected") 


# Attempt session creation
print("[] Opening a new session...")

receivedData.send(json.dumps({
    "id": 1,
    "jsonrpc": "2.0",
    "method": "createSession",
    "params": {
        "cortexToken": token,
        "headset": deviceID,
        "status": "open"
    }
}))

result = json.loads(receivedData.recv())["result"]
status = result["status"]
sessionID = result["id"]

if status == "opened":
    print("Session opened!")
else:
    raise Exception("[Error C2] Session not opened")


# Attempt session activation
print("[] Activating the session...")

receivedData.send(json.dumps({
    "id": 1,
    "jsonrpc": "2.0",
    "method": "updateSession",
    "params": {
        "cortexToken": token,
        "session": sessionID,
        "status": "active"
    }
}))

print("Session activated!")


# Subscribing to one or multiple data streams
print("[] Subscribing data stream for current session...")

receivedData.send(json.dumps({
    "id": 1,
    "jsonrpc": "2.0",
    "method": "subscribe",
    "params": {
        "cortexToken": token,
        "session": sessionID,
        "streams": ["dev"] 
    }
}))


eu = json.loads(receivedData.recv())["result"]["owner"]

initSerial()

sendMessage(eu)
msg = readMessage()
print(msg)

closeSerial()