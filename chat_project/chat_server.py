import asyncio

import websockets

connected_clients = set()


async def handle_connection(websocket, path):
    # Add the client to the set of connected clients
    connected_clients.add(websocket)

    try:
        # Notify all connected clients about the new user
        for client in connected_clients:
            await client.send(f"User {websocket.remote_address} joined the chat!")

        # Handle incoming messages
        async for message in websocket:
            # Broadcast the message to all connected clients
            for client in connected_clients:
                await client.send(f"{websocket.remote_address}: {message}")

    except websockets.exceptions.ConnectionClosedError:
        # Remove the client from the set upon disconnection
        connected_clients.remove(websocket)
        # Notify remaining clients about the user leaving
        for client in connected_clients:
            await client.send(f"User {websocket.remote_address} left the chat!")


start_server = websockets.serve(handle_connection, "localhost", 8765)

print("WebSocket chat server started. Listening on ws://localhost:8765")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
