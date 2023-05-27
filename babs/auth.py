# Transmitir dados entre PC e Servidor
import json 

# Conexão Segura
import ssl

# Para a conexão em si
from websocket import create_connection
import sys

# O primeiro passo é inicializar o objeto do tipo WebSocket.
# Pode ser feito usando apenas uma única função, create-connection.
try:
    print("Connecting to WebSocket...")
    receivedData = create_connection("wss://localhost:6868", sslopt={"cert_reqs": ssl.CERT_NONE})
except:
    print("Connection not Established")
    sys.exit(1)
    
# Agora temos que fazer um request ao WebSocket, mas primeiro precisamos de usar a função de enviar do WebSocket seguida de json.dumps e depois o request.
# Temos primeiro que enviar a autorização auth.py e receber uma resposta. Ao autorizar, vai-nos gerar um token que é a chave para executar outros pedidos.
receivedData.send(json.dumps({
    "jsonrpc": "2.0",
    "method": "getCortexInfo",
    "id": 1
}))
token = json.loads(receivedData.recv())["result"]
print(token)
print("\n")

receivedData.send(json.dumps({
    "jsonrpc": "2.0",
    "method": "getUserLogin",
    "id": 1
}))
UserLogin = json.loads(receivedData.recv())["result"]
print(UserLogin)
print("\n")

if not UserLogin:
    print("Unsuccessful login in EMOTIV Launcher!")
    sys.exit(1)
else:
    print("SUCCESSFUL LOGIN!")




receivedData.send(json.dumps({
    "jsonrpc": "2.0",
    "method": "queryHeadsets",
    "params": {},
    "id": 1
}))
print(receivedData.recv())


receivedData.send(json.dumps({
    "id": 1,
    "jsonrpc": "2.0",
    "method": "requestAccess",
    "params": {
        "clientId": "Kn0l81EmhItgtYievIS8cClHPVduYY0yXqQZk1u6",
        "clientSecret": "'K1JN2UNNovnJyY2kSt5CfUC8r5lp8Zpz9FBonzgQoOTefWgV1r22ZJXkJpwi4cHLE61pgUJpIz6oiu7f3cau5Hauk5A0VOApySqJbBqO9fF2k3YMjJbHJ8CxI4nRy2Tf"
    }
}))

try:
    wtoken = json.loads(receivedData.recv())["result"]["_auth"]
    print("access authorzed")
except:
    print("not granted access")
    sys.exit(1)


receivedData.send(json.dumps({
    "jsonrpc": "2.0",
    "method": "authorize",
    "params": {
        "clientId":"7I3iwjsiOtL3swJAIs9r21aeSUa66b0ZQ8IHD2hP",
        "clientSecret":"LxFdulB1MqdwluFXjTdLaf6pzDiQ0Kiog2JMJJGZ7CWs21WPb9qwcgAyJm6PGqV4EyLA7vzmKUlHHRjEJ7db0xOnQYrS2JR0ge5BrNRDwAn1RLjZA3Kcaxu35N5R3j4b"
    },
    "id": 1
}))
print(json.loads(receivedData.recv()))

try:
    wtoken = json.loads(receivedData.recv())["result"]["_auth"]
    print("authorized")
except:
    print("not granted authorization")
    sys.exit(1)


print("\nCreating session...")