import socket
import ssl
import os
import json

#server configuration settings
IP = "127.0.0.1"
PORT = 12345

def upload_file(client_socket):
    """Uploads a file to the server. """
    files_list = os.listdir()
    print(f"Available file to upload: {files_list}")

    file_name = input("Enter the file's name: ")
    while file_name not in files_list:
        #A loop that runs until the file name exists.
        file_name = input("There is no file with this name. ")

    with open(file_name, "rb") as file: #Opens the file and reads the content.
        data = file.read()
    
    client_socket.send(file_name.encode('utf-8'))
    client_socket.sendall(data)
    client_socket.send("<END>".encode('utf-8')) #A flag to tell the server that the upload is completerd.

def receive_file(client_socket):
    """Receives a file from the server. """
    files_list = json.loads(client_socket.recv(1024).decode('utf-8')) #The files available to download.
    print(f"Files avaiable: {files_list}")

    file_chosen = input("Enter the file's name: ")
    while file_chosen not in files_list:
        #A loop that runs until the wanted file exists.
        file_chosen = input("There is no file with this name: ")


    client_socket.send(file_chosen.encode('utf-8')) #Sends the choice.

    file_packets = b""

    while True:
        #A loop that runs until the file has been fully sent.
        data = client_socket.recv(1024)
        if not data or data == b"<END>":
            break
        file_packets += data

    #Creates the file.
    with open(file_chosen, "wb") as file:
        file.write(file_packets)

def client(client_socket):
    while True:
        #A loop that runs until the client wants to exit the program.
        os.system('cls') #Clears the terminal.
        while True:
            #A loop that runs until the choice is valid.
            choice = input("""
Enter your choice:
upload - upload a file to the server.
download - get a file from the server.
exit - exit the program. """)
            if choice.lower() == "upload" or choice.lower() == "download" or choice.lower() == "exit":
                break
            print("Invalid choice, choose one of the available choices. ")

        client_socket.send(choice.encode('utf-8'))

        if choice.lower() == "upload":
            upload_file(client_socket)
        elif choice.lower() == "download":
            receive_file(client_socket)
        elif choice.lower() == "exit":
            print("goodbye! ")
            break

def connect_to_server():
    #Connects to the server with ssl.
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False  # Disable hostname verification
    context.verify_mode = ssl.CERT_NONE  # Disable certificate verification

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_socket = context.wrap_socket(client_socket, server_hostname=IP)

    ssl_socket.connect((IP, PORT))
    try:
        client(ssl_socket)
        
    finally:
        ssl_socket.close()

if __name__ == '__main__':
    connect_to_server()
