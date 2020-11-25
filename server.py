import socket
import threading

BYTES = 1024
PORT = 5050
SERVER = '192.168.1.2'
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)
server.listen()

clients_list = []
name_list = []

def send_msg(msg):
    for client in clients_list:
        client.send(msg)

def handel_client(client):
    while True:
        try:
            msg = client.recv(BYTES)
            pMsg = msg.decode(FORMAT)
            print(pMsg)
            send_msg(msg)
        except:
            index = clients_list.index(client)
            clients_list.remove(client)
            client.close()
            name = name_list[index]
            print("[Client] {} Disconnected".format(name))
            send_msg('[SERVER] {} left!'.format(name).encode(FORMAT))
            name_list.remove(name)
            break

def receive():
    print("[STARTING] Server is tarting...")
    while True:
        client, address = server.accept()
        print(f"[NEW CONNECTION] {address} connected.")

        client.send('!NEWX_USERX'.encode(FORMAT))
        name = client.recv(BYTES).decode(FORMAT)
        name_list.append(name)
        clients_list.append(client)

        print("[New Client] Name is {}".format(name))
        client.send('[SERVER] Connected to server!'.encode(FORMAT))
        send_msg("[SERVER] {} joined!".format(name).encode(FORMAT))

        thread = threading.Thread(target=handel_client, args=(client,))
        thread.start()

receive()
