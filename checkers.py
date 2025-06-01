import pygame, sys
import asyncio
from game import Game
from server import AsyncServer

pygame.font.init()

"""Setting up for server"""
async def setup_server():
    server_ready = asyncio.Future()

    async def handle_client(reader, writer):
        server_ready.set_result((reader, writer))

    server = await asyncio.start_server(handle_client, '127.0.0.1', 5555)
    async with server:
        print("[SERVER] Waiting for opponent...")
        reader, writer = await server_ready
        network = AsyncServer(reader, writer)
        game = Game(network=network, is_server=True)
        await game.main()

"""Setting up for client"""
async def setup_client():
    ip = input("Enter server IP: ")
    reader, writer = await asyncio.open_connection(ip, 5555)
    network = AsyncServer(reader, writer)
    game = Game(network=network, is_server=False)
    await game.main()

async def run_game():
    is_server = input("Host or Join? (h/j): ").strip().lower() == 'h'
    if is_server:
        await setup_server()
    else:
        await setup_client()


if __name__ == "__main__":
    asyncio.run(run_game())