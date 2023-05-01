import socket
import keyboard
import threading


class ButtonCheckerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if keyboard.is_pressed('q'):
                msg = input()
                send(msg)

# header size(amount of bites to be received from client)
HEADER = 64

# format used
FORMAT = 'utf-8'

# disconnection message
DISCONNECT_MESSAGE = "!DISCONNECT!"

# setting port no
PORT  = 5050

# geting server IP
SERVER = socket.gethostbyname(socket.gethostname())
print(" it is the server address :" + SERVER)

# creating a tupel address which consist of server IP and PORT no
ADDR = (SERVER, PORT)

# family and type (types of address we are looking for)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# binding the address to this socket so anything comes to this address hit this socket
server.bind(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    return (send_length,message)


def handel_client(conn, addr):
    # who connected
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        # a blocking line of code waiting to receive info from client in sleep so other threads do not get blocked.
        # as the message is converted into byte format before transmitting we have to decode it in original format.
        msg_length = conn.recv(HEADER).decode(FORMAT)


        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] {msg}")
            conn.send("Message Received".encode(FORMAT))

            # disconnect issue: a client can disconnect without telling the server any there is not much of a problem.
            # but when it tries to reconnect the server gets confuse that why it's requesting again.
            if msg == DISCONNECT_MESSAGE:
                connected = False
    conn.close()


def start():
    # it listens to the socket that what connections are comming
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER}")
    # now it will listen continuously or till the server crasher or shutdown for new connections
    while True:
        # it waits for the  new connection to connect to the socket.
        # it saves it's address(IP and PORT no)
        # conn(which is a socket object) will store info and allow us to send information back to the connection.
        # it is a blocking line of code the thread sleeps until notified by the event it is expecting.
        conn, addr = server.accept()

        # now clients will be handles using multithreading(runs concurrently)
        thread = threading.Thread(target=handel_client, args=(conn, addr))
        thread.start()

        # activeCount - 1 coz first thread will be listing to all the connections.
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

print("[STARTING SERVER] initiating.....")
start()