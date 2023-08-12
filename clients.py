import socket
import threading
import os


def enter_server():
    os.system('cls||clear')
    global nickname

    nickname = input("Choose Your Nickname:")

    # Store the ip and port number for connection
    ip = "127.0.0.1"
    port = 5555
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to a host
    client.connect((ip, port))

stop_thread = False


def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                # Clients those are banned can't reconnect
            else:
                print(message)
        except socket.error:
            print('Error Occured while Connecting')
            client.close()
            break


def write():
    while True:
        if stop_thread:
            break
        # Getting Messages
        # message = f'{nickname}: {input("")}'
        message = input("")
        client.send(message.encode('ascii'))

enter_server()
receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
