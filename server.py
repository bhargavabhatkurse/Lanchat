import socket
import threading

def handle_client(client_socket, client_address):
    while True:
        try:
            # Receive message from the client
            message = client_socket.recv(1024).decode('utf-8')

            if not message:
                # Handle client disconnection
                print(f'{client_address[0]}:{client_address[1]} - Disconnected')
                client_socket.close()
                break

            print(f'{client_address[0]}:{client_address[1]} - {message}')

            # Broadcast the received message to all clients
            broadcast(message, client_socket)

        except ConnectionResetError:
            # Handle client disconnection
            print(f'{client_address[0]}:{client_address[1]} - Disconnected')
            client_socket.close()
            break

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                # Send message to other clients
                client.send(message.encode('utf-8'))
            except:
                # Handle client disconnection
                client.close()
                clients.remove(client)

# Server configuration
HOST = '127.0.0.1'  # Listen on all available network interfaces
PORT = 5555

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

print(f'Server started on {HOST}:{PORT}')

clients = []
is_running = True  # Variable to control the server's running state

def stop_server():
    global is_running
    is_running = False
    # Close all client sockets
    for client_socket in clients:
        client_socket.close()
    # Close the server socket
    server_socket.close()

# Start a separate thread to listen for the stop command
def stop_thread():
    while is_running:
        command = input("Enter 'stop' to stop the server: \n")
        if command.strip().lower() == 'stop':
            stop_server()

threading.Thread(target=stop_thread).start()

while is_running:
    # Accept a new connection
    client_socket, client_address = server_socket.accept()
    print(f'New connection from {client_address[0]}:{client_address[1]}')

    # Add the new client to the list
    clients.append(client_socket)

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
