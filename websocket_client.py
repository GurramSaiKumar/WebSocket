import asyncio
import websockets


async def connect_and_send():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri, timeout=100) as websocket:
        print(f"Connected to {uri}")
        # Sending messages to the server
        await websocket.send("Hello, baby!")
        # Receiving messages from the server
        response = await websocket.recv()
        print(f"Received from server: {response}")


asyncio.get_event_loop().run_until_complete(connect_and_send())
