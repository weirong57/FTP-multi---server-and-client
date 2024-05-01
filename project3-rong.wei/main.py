import socket
import threading
import pickle

class ClientServer:
    def __init__(self, name):
        # Initialize the class with the user's name and set up the server and client sockets.
        self.name = name  # User's name
        self.server_socket = None
        self.client_socket = None
        self.server_port = 0  # This will store the dynamically assigned port
        self.start_server()

    def start_server(self):
        # Set up the server: create a socket, bind to localhost with an available port, and start listening.
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 0))  # Bind to localhost and a random available port
        self.server_socket.listen(1)
        self.server_port = self.server_socket.getsockname()[1]
        print(f"Your chat server port number is {self.server_port}")
        # Start a new thread to accept connections, allowing the main thread to do other tasks.
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        # Continuously accept new client connections and handle each client in a new thread.
        while True:
            client, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()

    def handle_client(self, client_socket):
        # Handle communication with a connected client.
        with client_socket, client_socket.makefile('rb') as client_stream:
            while True:
                try:
                    # Receive data from the client.
                    command, data = pickle.load(client_stream)
                    if command == 'chat':
                        # Print chat messages.
                        print(f"Message from {data[0]}: {data[1]}")
                    elif command == 'file':
                        # Receive files and save them with the prefix 'received_'.
                        filename = data
                        with open(f"received_{filename}", 'wb') as f:
                            while True:
                                chunk = pickle.load(client_stream)
                                if chunk == b'END':
                                    break
                                f.write(chunk)
                        print(f"File {filename} received.")
                except EOFError:
                    # Handle client disconnection.
                    print("Client disconnected.")
                    break

    def connect_to_server(self, host, port):
        # Connect to a specified server.
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        print(f"Connected to server {host}:{port}")
        # Start a thread to receive messages from the server.
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        # Receive messages from the server.
        with self.client_socket, self.client_socket.makefile('rb') as client_stream:
            while True:
                try:
                    command, data = pickle.load(client_stream)
                    if command == 'chat':
                        print(f"Received message from {data[0]}: {data[1]}")
                    elif command == 'file':
                        filename = data
                        with open(f"received_{filename}", 'wb') as f:
                            while True:
                                chunk = pickle.load(client_stream)
                                if chunk == b'END':
                                    break
                                f.write(chunk)
                        print(f"File {filename} received.")
                except EOFError:
                    print("Disconnected from server.")
                    break

    def send_chat(self, message):
        # Send a chat message to the server.
        with self.client_socket.makefile('wb') as client_stream:
            pickle.dump(('chat', (self.name, message)), client_stream)
            client_stream.flush()

    def send_file(self, filename):
        # Send a file to the server.
        with self.client_socket.makefile('wb') as client_stream:
            pickle.dump(('file', filename), client_stream)
            with open(filename, 'rb') as f:
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break
                    pickle.dump(chunk, client_stream)
                pickle.dump(b'END', client_stream)
                client_stream.flush()
            print(f"File {filename} sent.")

def main():
    # Main function to run the application.
    name = input("Enter your name: ")  # Prompt the user for their name at the start.
    client_server = ClientServer(name)
    print("Ready to connect to the server.")
    host = input("Enter the host to connect to (leave blank for localhost): ") or 'localhost'

    # Get the port number to connect to and handle input errors.
    while True:
        port_input = input("Please enter the port number to connect: ")
        if port_input:
            try:
                port = int(port_input)
                break
            except ValueError:
                print("Invalid input, please enter a valid integer port number!")
        else:
            print("No port number entered, please enter a port number.")

    client_server.connect_to_server(host, port)

    # Provide options for user interaction.
    while True:
        action = input("Choose action: Send message (1), Send file (2), Exit (3): ")
        if action == '1':
            message = input("Enter message: ")
            client_server.send_chat(message)
        elif action == '2':
            filename = input("Enter filename: ")
            client_server.send_file(filename)
        elif action == '3':
            break

if __name__ == '__main__':
    main()
