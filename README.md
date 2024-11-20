# Secure File Transfer

This project is a **file transfer application** that allows secure file uploads and downloads between a client and server using SSL/TLS. The server hosts files in a designated folder, and the client can interact with the server to upload or download files.

---

## Features

- **Secure Communication**: Uses SSL/TLS to encrypt data transferred between the client and server.
- **Upload Files**: Clients can upload files to the server.
- **Download Files**: Clients can browse and download files stored on the server.
- **User-Friendly Interface**: Clear prompts for user interaction.
- **File Integrity**: Ensures that file transfers are complete and accurate.

---

## Requirements

- **Python 3.8+**
- Required Libraries:
  - `socket`
  - `ssl`
  - `os`
  - `json`
- SSL Certificate and Key:
  - A valid certificate (`server.crt`) and key (`server.key`) are required for the server (for testing purposes a self made certificate is also fine).

---

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/secure-file-transfer.git
cd secure-file-transfer
```
### 2. Generate SSL Cetificates
You can generate a self-signed certificate using OpenSSL:

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt
```

### 3. Create the Server's Files Directory

Ensure you have a folder to store server files. Update the files_folder variable in the server script to reflect its path:

```python
  files_folder = r"C:\path\to\server\files"
```

## Usage

### 1. Start the Server
Run the server script on the machine hosting the files:
```bash
python server.py
```
The server will listen on 127.0.0.1:12345.

### 2. Run the Client
Run the client script on another machine or the same machine:

```bash
python client.py
```
**Make sure to run it in this directory only.**

### 3. Interact With the Server
The client will prompt for the following actions:

-upload: Upload a file to the server.

-download: Download a file from the server.

-exit: Exit the application.

## File Flow

### Upload
1. Client selects a file from their local directory.
2. The file is sent to the server over an encrypted connection.
3. The server saves the file to its designated directory.

### Download
1. Server sends a list of available files to the client.
2. Client selects a file to download.
3. The file is transferred securely to the client's machine.



