import asyncio
import json
import websockets

# Maintain a set of connected clients
connected_clients = set()


async def handle_drawing(websocket, path):
    connected_clients.add(websocket)

    try:
        # Continuously listen for messages from the client
        while True:
            message = await websocket.recv()
            # Broadcast the received message to all connected clients
            await broadcast(message)
    finally:
        # Remove the client from the set when the WebSocket connection is closed
        connected_clients.remove(websocket)


async def broadcast(message):
    # Send the message to all connected clients
    for client in connected_clients:
        try:
            await client.send(message)
        except websockets.exceptions.ConnectionClosedError:
            connected_clients.remove(client)


if __name__ == "__main__":
    server = websockets.serve(handle_drawing, "localhost", 8765)
    print("WebSocket drawing server started. Listening on ws://localhost:8765")

    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()
