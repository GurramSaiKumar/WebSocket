import asyncio
import websockets


async def handle_connection(websocket, path):
    # This function will be called whenever a new WebSocket connection is established
    print(f"Client connected: {websocket.remote_address}")

    try:
        # Handle incoming messages
        async for message in websocket:
            print(f"Received message from {websocket.remote_address}: {message}")
            response = f"Server received: {message}"
            await websocket.send(response)

    except websockets.exceptions.ConnectionClosedError:
        print(f"Connection with {websocket.remote_address} closed")


start_server = websockets.serve(handle_connection, "localhost", 8765)

print("WebSocket server started. Listening on ws://localhost:8765")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
