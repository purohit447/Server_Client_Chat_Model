import socket

# header size(amount of bites to be received from client)
HEADER = 64

# format used
FORMAT = 'utf-8'

# disconnection message
DISCONNECT_MESSAGE = "!DISCONNECT!"

# setting port no
PORT  = 5050

# server
SERVER = "192.168.10.63"

# address
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

send("AllHailChimmanlal")