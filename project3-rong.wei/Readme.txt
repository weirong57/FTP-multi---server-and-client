
# Chat and File Transfer System

This system allows users to chat and transfer files between a server and a client over a network. The server must be started before the client can connect. The scripts are written in Python and include functionality for real-time messaging and file transfers.

## Getting Started

### Prerequisites

Ensure that Python is installed on your system. This script is compatible with Python 3.x.

### Running the Server

1. Open a command prompt or terminal.
2. Navigate to the directory containing the script.
3. Run the server script by entering the following command:
   ```shell
   python main.py
   ```
4. The server will automatically choose an available port and listen for connections.

### Running the Client

1. Open a new command prompt or terminal window.
2. Navigate to the directory containing the script.
3. Start the client script by running:
   ```shell
   python main.py
   ```
4. Enter your name when prompted.
5. Enter the hostname (usually `localhost` if running locally) and the port number displayed by the server.

## Operations

After connecting, you can perform the following operations via the client interface:

- **Send Message (m)**: Type 'm' and enter your message to send it to the connected server.
- **Send File (f)**: Type 'f' and provide the file path to send a file to the server. The server will save the file with a 'received_' prefix to distinguish it.
- **Exit (q)**: Type 'q' to safely disconnect from the server.

Each operation will prompt you for additional input as needed. Follow the on-screen instructions to communicate or transfer files.

## Example Usage

- Start the server:
  ```shell
  \path\to\project> python main.py
  Enter your name: ServerName
  Your chat server port number is 12345
  ```

- Connect the client and interact:
  ```shell
  \path\to\project> python main.py
  Enter your name: ClientName
  Ready to connect to the server.
  Enter the host to connect to (leave blank for localhost): localhost
  Please enter the port number to connect: 12345
  Connected to server localhost:12345
  Choose action: Send message (m), Send file (f), Exit (q): m
  Enter message: Hello, Server!
  ```

Follow these prompts to continue interacting with the server, send files, or receive messages. Exit the client or server using the 'q' command when done.

---
