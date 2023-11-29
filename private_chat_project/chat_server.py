import asyncio
import websockets

connected_users = {}


async def handle_connection(websocket, path):
    user_id = await register_user(websocket)
    connected_users[user_id] = websocket

    # Notify all connected clients about the new user
    for client in connected_users.values():
        await client.send(f"User {user_id} joined the chat!")

    try:
        # Handle incoming messages
        async for message in websocket:
            # Detect private messages
            if message.startswith('@'):
                recipient_id, private_message = parse_private_message(message)
                if recipient_id in connected_users:
                    recipient_ws = connected_users[recipient_id]
                    await recipient_ws.send(f"{user_id} (private): {private_message}")
                else:
                    await websocket.send(f"User {recipient_id} not found.")
            else:
                # Broadcast regular messages to all connected clients
                for client in connected_users.values():
                    await client.send(f"{user_id}: {message}")

    except websockets.exceptions.ConnectionClosedError:
        # Remove the user upon disconnection
        del connected_users[user_id]
        # Notify remaining clients about the user leaving
        for client in connected_users.values():
            await client.send(f"User {user_id} left the chat!")


async def register_user(websocket):
    await websocket.send("Welcome to the chat! Please enter your username:")
    user_id = await websocket.recv()
    return user_id


def parse_private_message(message):
    recipient_id, private_message = message.split(' ', 1)
    return recipient_id[1:], private_message


start_server = websockets.serve(handle_connection, "localhost", 8765)

print("WebSocket chat server started. Listening on ws://localhost:8765")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
