import asyncio
import websockets
from flask import Flask, request, render_template

app = Flask(__name__)

# Create a list to store all connected WebSocket clients
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/broadcast', methods=['POST'])
def broadcast_message():
    #message = request.form.get('message')
    message = "Hi"
    if message:
        # Broadcast the message to all connected WebSocket clients
        for client in connected_clients:
            asyncio.create_task(client.send(message))
        return 'Message broadcasted successfully'
    else:
        return 'No message provided', 400

# Start the WebSocket server
start_server = websockets.serve(ws_handler, "bettingsocket-d89de658d946.herokuapp.com",60000)

if __name__ == '__main__':
    #app.run(host='localhost', port=443, debug=True, threaded=True)
    # Start the WebSocket server in a separate event loop
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
    #asyncio.run(start_server)
