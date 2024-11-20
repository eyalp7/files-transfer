import socket
import ssl
import os
import json

#Server configuration settings.
IP = "127.0.0.1"
PORT = 12345

files_folder = r"C:\Users\User\Desktop\files" #The folder that holds the server's files.

def receive_file(client_socket):
    """Receives a file from the client. """
    file_name = client_socket.recv(1024).decode('utf-8')
    file_packets = b""

    while True:
        #A loop that runs until the file is fully sent.
        data = client_socket.recv(1024)
        if not data or data == b"<END>":
            break

        file_packets += data

    with open(os.path.join(files_folder, file_name), "wb") as file: #Creates a file and writes in it.
        file.write(file_packets)


def upload_file(client_socket):
    """Sends a file to the client. """
    files_list = os.listdir(files_folder) #All of the files in the directory.
    client_socket.send(json.dumps(files_list).encode('utf-8'))

    file_name = client_socket.recv(1024).decode()
    file_path = os.path.join(files_folder, file_name) #The absolute path of the file.

    with open(file_path, "rb") as file:
        data = file.read()
    
    client_socket.sendall(data)
    client_socket.send("<END>".encode('utf-8'))


def handle_client(client_socket):
    """Handles the main communication with the client. """
    while True:
        #A loop that runs until the client leaves.
        choice = client_socket.recv(1024).decode('utf-8')

        if choice == "upload":
            receive_file(client_socket)
        elif choice == "download":
            upload_file(client_socket)
        elif choice == "exit":
            break

def start_server():
    """Starts a server with ssl implemented."""
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key") #Using the key and the certificate.

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))

    server_socket.listen(1)
    print(f"Server is listening on {IP}:{PORT}...")

    while True:
        connection, address = server_socket.accept()
        print(f"Connection established from {address}")

        ssl_connection = context.wrap_socket(connection, server_side=True)

        handle_client(ssl_connection)
        print("client disconnected. ")

if __name__ == "__main__":
    start_server()
