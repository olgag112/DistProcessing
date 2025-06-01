# async_network.py
import asyncio
import pickle
import struct


class AsyncNetwork:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    async def send(self, data):
        try:
            serialized = pickle.dumps(data)
            length = struct.pack('>I', len(serialized))
            self.writer.write(length + serialized)
            await self.writer.drain()
        except Exception as e:
            print("Send failed:", e)

    async def receive(self):
        try:
            raw_length = await self.reader.readexactly(4)
            length = struct.unpack('>I', raw_length)[0]
            data = await self.reader.readexactly(length)
            return pickle.loads(data)
        except Exception as e:
            print("Receive failed:", e)
            return None

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()
