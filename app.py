import websockets
import asyncio
import os
 
# Creating WebSocket server
connected_clients = []

# WebSocket server
async def ws_handler(websocket, path):
    # Add the new client to the list of connected clients
    connected_clients.append(websocket)
    print(f"New client connected, total clients: {len(connected_clients)}")

    try:
        async for message in websocket:
            # Broadcast the received message to all connected clients
            for client in connected_clients:
                await client.send(message)
    finally:
        # Remove the client from the list of connected clients when disconnected
        connected_clients.remove(websocket)
        print(f"Client disconnected, total clients: {len(connected_clients)}")


 
async def main():
    async with websockets.serve(ws_handler, "bettingsocket-d89de658d946.herokuapp.com", os.environ.get('PORT')):
        print(f"PORT SET")
        await asyncio.Future()  # run forever
 
if __name__ == "__main__":
    asyncio.run(main())
