import socket
import threading

host = '127.0.0.1'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, 9999))

server.listen()

clients = []
nicknames = []
# client, addr = server.accept()

# done = False

# while not done:
#     msg = client.recv(1024).decode('utf-8')
#     if msg == 'quit':
#         done = True
#     else:
#         print(msg)
#     client.send(input("Message: ").encode('utf-8'))

# client.close()

# server.close()

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")

        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickanme of client is {nickname}")
        broadcast(f"{nickname} has joined the chat!".encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is listening...')
receive()