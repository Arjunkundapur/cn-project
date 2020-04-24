import socket
import tqdm
import os
from cryptography.fernet import Fernet

def create_socket():
    try:
        global host
        global port
        global s
        host = "0.0.0.0"
        port = 8921
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))

def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the port: " + str(port))
        s.bind((host,port))
        s.listen(5)
        print(f"[*] Listening on {host}:{port}")
    except socket.error as msg:
        print("Socket binding error: " + str(msg))
        # print("Retrying...")
        # bind_socket()
        
def load_key():
    #loads the key from the current directory named `key.key`
    return open("key.key", "rb").read()

def decrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()			# read the encrypted data
 
    decrypted_data = f.decrypt(encrypted_data)		# decrypt data
    with open(filename, "wb") as file:
        file.write(decrypted_data)		        # write the original file

def socket_accept():
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"
    global s
    client_socket, address = s.accept() 
    print("Connection has been established: " + "IP " + str(address[0]) + " |Port " + str(address[1]))
    received = client_socket.recv(BUFFER_SIZE).decode()
    fileName, fileSize = received.split(SEPARATOR)
    fileName = os.path.basename(fileName)
    fileSize = int(fileSize)

    progress = tqdm.tqdm(range(fileSize), f"Receiving {fileName}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(fileName, "wb") as f:
        for _ in progress:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:    
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))

    client_socket.close()
    s.close()
    return fileName

def main():
    create_socket()
    key = load_key()
    bind_socket()
    fileName = socket_accept()
    decrypt(fileName,key)
main()






    