import json                                 # Data format trasmission package
import ssl                                  # Machine and server secure connection package
from websocket import create_connection     # Machine and server connection type package
import sys                                  # System tools package


# Obtained from: https://www.emotiv.com/my-account/cortex-apps/
your_app_client_id = 'Kn0l81EmhItgtYievIS8cClHPVduYY0yXqQZk1u6'
your_app_client_secret = 'K1JN2UNNovnJyY2kSt5CfUC8r5lp8Zpz9FBonzgQoOTefWgV1r22ZJXkJpwi4cHLE61pgUJpIz6oiu7f3cau5Hauk5A0VOApySqJbBqO9fF2k3YMjJbHJ8CxI4nRy2Tf'

print("Initializing...")

# Establish a WebSocket connection
print("[1/5] Connecting to websocket...")

try:
    receivedData = create_connection("wss://localhost:6868", sslopt={"cert_reqs": ssl.CERT_NONE})
    print("Connection established!")

except Exception as e:
    print("[Error A1] WebSocket connection:", str(e))
    sys.exit(1)
    # Reinstall EMOTIV software 


# Verify if installation is done correctly
print("[2/5] Verifying Cortex installation...")

receivedData.send(json.dumps({
    "id":1,
    "jsonrpc":"2.0",
    "method":"getCortexInfo"
    }))

cortexInfo = json.loads(receivedData.recv())["result"]

if cortexInfo:
    print("Correct installation!")
else:
    raise Exception("[Error A2] EMOTIV installation")
    # Reinstall EMOTIV software


# Verify if user login in EMOTIV Launcher is done correctly
print("[3/5] Connecting to EMOTIV Launcher...")

receivedData.send(json.dumps({
    "id":1,
    "jsonrpc":"2.0",
    "method":"getUserLogin"
    }))

userInfo = json.loads(receivedData.recv())["result"]

if userInfo:
    print("Successful login in EMOTIV Launcher!")
else:
    raise Exception("[Error A3] EMOTIV Launcher login")
    # Open EMOTIV Launcher and login
    

# Request application access
print("[4/5] Requesting EMOTIV Launcher access...")

receivedData.send(json.dumps({
    "jsonrpc": "2.0",
    "method": "requestAccess",
    "params": {
        "clientId": your_app_client_id,
        "clientSecret": your_app_client_secret
    },
    "id": 1
}))

access = json.loads(receivedData.recv())["result"]["accessGranted"]

if(access):
    print("Access granted!")
else:
    raise Exception("[Error A4] EMOTIV Launcher access")
    # Open EMOTIV Launcher and accept request


# Request authentication token (authorization for other requests)
print("[5/5] Requesting Cortex API authorization...")

receivedData.send(json.dumps({
    "jsonrpc": "2.0",
    "method": "authorize",
    "params": {
        "clientId": your_app_client_id,
        "clientSecret": your_app_client_secret
    },
    "id": 1
}))

try:
    token = json.loads(receivedData.recv())["result"]["cortexToken"]
    print("Authorization granted!")

except:
    raise Exception("[Error A5] Cortex API authorization")
    # Read API


print("Initialized with success!")