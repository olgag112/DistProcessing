import pickle
import struct

# mutual functions for sending/receiving sockets

async def send_with_length(writer, data):
    try:
        serialized = pickle.dumps(data)
        length = struct.pack('>I', len(serialized))
        writer.write(length + serialized)
        await writer.drain()
    except Exception as e:
        print("Send failed:", e)

async def receive_with_length(reader):
    try:
        raw_length = await reader.readexactly(4)
        length = struct.unpack('>I', raw_length)[0]
        data = await reader.readexactly(length)
        return pickle.loads(data)
    except Exception as e:
        print("Receive failed:", e)
        return None
