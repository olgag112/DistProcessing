import socket
import pickle
import struct

def send_with_length(sock, data):
    try:
        serialized = pickle.dumps(data)
        length = struct.pack('>I', len(serialized))  # 4-byte big-endian
        sock.sendall(length + serialized)
    except Exception as e:
        print("Send failed:", e)

def recv_with_length(sock):
    try:
        # Read message length (first 4 bytes)
        raw_length = recvall(sock, 4)
        if not raw_length:
            return None
        length = struct.unpack('>I', raw_length)[0]
        # Read the full message data based on length
        data = recvall(sock, length)
        return pickle.loads(data)
    except Exception as e:
        print("Receive failed:", e)
        return None

def recvall(sock, n):
    """Helper to receive n bytes or return None if EOF is hit"""
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
        return recv_with_length(self.client)

    def close(self):
        self.client.close()
