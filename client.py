import socket
import pickle
import struct

def send_with_length(sock, data):
    try:
        # convert data into bytes
        serialized = pickle.dumps(data)
        # add a length of data
        length = struct.pack('>I', len(serialized))
        # send length of data and data
        sock.sendall(length + serialized)
    except Exception as e:
        print("Send failed:", e)

def reiceve_with_length(sock):
    try:
        # reading the length of data
        raw_length = reiceve_all(sock, 4)
        if not raw_length:
            return None
        length = struct.unpack('>I', raw_length)[0]
        # Read the full message data based on length
        data = reiceve_all(sock, length)
        # convert bytes into data
        return pickle.loads(data)
    except Exception as e:
        print("Receive failed:", e)
        return None

# Waiting for all data to come
def reiceve_all(sock, n):
    data = b''
    while len(data) < n:
        try:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        except BlockingIOError:
            continue
    return data


class Client:
    def __init__(self, server_ip, port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client.connect((server_ip, port))
        print(f"Connected to server {server_ip}")
        self.client.setblocking(False)

    def send(self, data):
        send_with_length(self.client, data)

    def receive(self):
        return reiceve_with_length(self.client)

    def close(self):
        self.client.close()
