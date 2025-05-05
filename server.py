# server.py
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

# Helper to receive n bytes or return None if EOF is hit
def recvall(sock, n):
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


class Server:
    def __init__(self, host='', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(1)
        print(f"[SERVER] Waiting for connection on port {port}...")
        self.conn, self.addr = self.server.accept()
        print(f"[SERVER] Connected to {self.addr}")

    def send(self, data):
     send_with_length(self.conn, data)

    def receive(self):
        return recv_with_length(self.conn)
