# server.py
import socket
import pickle
import struct
from forwarding import *

class AsyncServer:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    async def send(self, data):
        await send_with_length(self.writer, data)

    async def receive(self):
        return await receive_with_length(self.reader)
