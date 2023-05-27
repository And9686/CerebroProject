# Usar pedidos de autorização
from auth import token

# Criar delays entre cada deteção ao treinar os comandos
import time

# Libraria para controlar um cursor e teclado
import pyautogui

print("Checking headset connectivity...")receivedData.send(json.dumps({
    "jsonrpc": "2.0",
    "method": "queryHeadsets",
    "params": {},
    "id": 1
}))print(receivedData.recv())print("\nCreating session...")receivedData.send(json.dumps({
    "jsonrpc": "2.0",
    "method": "createSession",
    "params": {
        "_auth": token,
        "status": "open",
        "project": "test"
    },
    "id": 1
}))print(receivedData.recv())print("\nSubscribing to session...")receivedData.send(json.dumps({
    "jsonrpc": "2.0",
    "method": "subscribe",
    "params": {
        "_auth": token,
        "streams": [
            "sys"
        ]
    },
    "id": 1
}))print(receivedData.recv())print("\nGetting detection info...")receivedData.send(json.dumps({
    "jsonrpc": "2.0",
    "method": "getDetectionInfo",
    "params": {
        "detection": "mentalCommand"
    },
    "id": 1
}))print(receivedData.recv())