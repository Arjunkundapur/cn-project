# File transfer with authentication

## Installation/set-up
1. Use pip to install the specified libraries mentioned in `requirements.txt` \
   `pip3 install -r requirements` on a typical Linux/Unix machine.

## Running 

### 1. Client
1. Open a terminal in the client directory
2. Generate the key.key file by running the following command \
   `python3 client.py generate`
3. Run the client file after running the server file \
   `python3 client.py`

### 2. Server
1. Copy the generated `key.key` from the client folder into the server folder
2. Open a terminal in the server directory
3. Run the server file \
   `python3 server.py`

# Note:
The client and server files can be run on separate machines, after updating the hostname in the respective files.
