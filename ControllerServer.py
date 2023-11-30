import socket
import threading
import time
from queue import Queue

HOST = '127.0.0.1'
PORT = 8888
PT_OP = PORT
SOCK = []  # List to store sockets
CLIENTS = []  # List to store client addresses
MSVR = False
Mclient = 0  # Main client count
input_queue = Queue()

class EchoServerClientProtocol:
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))
        self.transport.write(data)

def CheckPort(port):
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = False
    try:
        sc.bind((HOST, port))
        result = True
    except:
        result = False
    sc.close()
    return result

def AllocatePort():
    global PT_OP
    while True:
        PT_OP += 1
        if CheckPort(PT_OP):
            return PT_OP

        if (PT_OP - PORT) > 1000:
            break

def mainServer():
    global Mclient
    Mclient += 1

    # Create a new socket for each client
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        c.bind((HOST, PORT))
        c.listen(1)
        print(f'> Main server started: {HOST}({PORT})')

        z, b = c.accept()
        print(f'Client connected: {b}')

        data = z.recv(1024)  # Assuming a buffer size of 1024

        user_input = input_queue.get()  # Retrieve input from the queue
        value = int(user_input)

        if value == 0:
            exit()
        elif value == 1:
            print('Creating new thread')
            PT_OP = AllocatePort()
            z.send(f'port{PT_OP}'.encode())  # Sending data back to the client
        elif value == 2:
            # Perform memoized Fibonacci calculation
            n = 100
            start_time = time.time()
            result_memoized = memoized_fibonacci(n)
            end_time = time.time()
            response = f"Memoized Fibonacci result: {result_memoized}, Time taken: {end_time - start_time} seconds"
            z.send(response.encode())  # Sending data back to the client
        elif value == 3:
            protocol = EchoServerClientProtocol()
            protocol.connection_made(z)
            protocol.data_received(data)

def ServerThreads(host, port):
    global SOCK, CLIENTS
    try:
        d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        d.bind((host, port))
        d.listen(1)
        s, a = d.accept()
        CLIENTS.append(a)
        SOCK.append(s)
        print('Client connected:', a)

    except:
        exit()

def memoized_fibonacci(n, arr={}):
    if n in arr:
        return arr[n]
    if n <= 0:
        arr[n] = 0
    elif n == 1:
        arr[n] = 1
    else:
        arr[n] = memoized_fibonacci(n - 1, arr) + memoized_fibonacci(n - 2, arr)
    return arr[n]

while True:
    if not MSVR:
        mainServerThread = threading.Thread(name='mainServer', target=mainServer)
        mainServerThread.start()
        MSVR = True

        user_input = input("Enter a value:")
        input_queue.put(user_input)  # Put user input into the queue

    # Example of creating additional server threads (you can adjust the parameters accordingly)
    thread = threading.Thread(target=ServerThreads, args=(HOST, PORT + 1))
    thread.start()
