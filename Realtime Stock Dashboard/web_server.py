import asyncio
import json

import websockets
from stock_price import get_stock_price

connected_clients = set()


async def register_client(websocket):
    connected_clients.add(websocket)
    print(f"Client {websocket.remote_address} connected")


async def unregister_client(websocket):
    connected_clients.remove(websocket)
    print(f"Client {websocket.remote_address} disconnected")


company_with_client_mapping = dict()


async def push_updates(websocket, path):
    await register_client(websocket)

    async def receive_messages():
        while True:
            payload = await websocket.recv()
            request_data = json.loads(payload)
            await construct_company_with_symbols_mapping(request_data, websocket)

    async def send_updates():
        while True:
            for company in company_with_client_mapping:
                # stock_price = get_stock_price(company)
                stock_price = 150
                message = json.dumps({"symbol": company, "price": stock_price})
                clients = company_with_client_mapping[company]
                disconnected_clients = set()
                for client in clients:
                    try:
                        await client.send(message)
                    except websockets.exceptions.ConnectionClosedOK:
                        disconnected_clients.add(client)
                for disconnected_client in disconnected_clients:
                    await unregister_client(disconnected_client)
            await asyncio.sleep(25)

    await asyncio.gather(receive_messages(), send_updates())


async def construct_company_with_symbols_mapping(request_data, websocket):
    symbol = request_data.get('symbol')
    if symbol in company_with_client_mapping:
        company_with_client_mapping[symbol].append(websocket)
    else:
        value = [websocket]
        company_with_client_mapping[symbol] = value


server = websockets.serve(push_updates, 'localhost', 8745)
print("WebSocket chat server started. Listening on ws://localhost:8745")
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
