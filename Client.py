import socket

HOST = '127.0.0.1'
PORT = 8888

def connect_to_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print(f'Connected to server: {HOST}({PORT})')

        request = input("Enter a value (0 to exit, 1 for a new thread, 2 for memoized Fibonacci, 3 for computer infomation): ")
        client_socket.send(request.encode())

        if request == '0':
            print('Exiting...')
            return

        response = client_socket.recv(1024).decode()
        print(f'Server response: {response}')

if __name__ == "__main__":
    connect_to_server()
