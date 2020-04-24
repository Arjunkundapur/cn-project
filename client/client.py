# Install pip3
# from pip3 install tqdm lib for loader. if linux - sudo apt-get pip3, pip3 install tqdm
# if loader not necessary, remove loader code and run directly

# client is the sender and server is the receiver
import socket
import tqdm
import os
from cryptography.fernet import Fernet


def create_socket():
    try:
        global host
        global port
        global s
        host = "localhost"  # enter ip of server
        port = 8921
        s = socket.socket()
    except:
        print("Socket creation error")


def connect_to_server():
    try:
        global host
        global port
        global s
        print("Connecting to: " + str(host) + ":" + str(port))
        s.connect((host, port))
        print("Connected")
    except:
        print("error while connecting to server")


def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    return open("key.key", "rb").read()


def encrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
        encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)


def decrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = f.decrypt(encrypted_data)
    with open(filename, "wb") as file:
        file.write(decrypted_data)


def send_file():
    global s
    global fileName
    fileSize = os.path.getsize(fileName)
    print("filesize", fileSize)
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096  # sending 4096 bytes each time step
    s.send(f"{fileName}{SEPARATOR}{fileSize}".encode())

    progress = tqdm.tqdm(range(
        fileSize), f"Sending {fileName}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(fileName, "rb") as f:
        bytes_read = f.read(BUFFER_SIZE)
        for _ in progress:
            if not bytes_read:
                break
            s.sendall(bytes_read)
            progress.update(len(bytes_read))
    s.close()


def generate_key():
    import sys
    if(len(sys.argv) > 1 and sys.argv[1] == "generate"):
        write_key()
        return True


def main():
    if (generate_key()):
        return
    global fileName
    fileName = "samplefile.csv"
    create_socket()
    connect_to_server()
    key = load_key()
    encrypt(fileName, key)
    send_file()
    decrypt(fileName, key)


if __name__ == "__main__":
    main()
