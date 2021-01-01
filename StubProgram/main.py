from encryption import get_login_password
import asyncio
import websockets
from websockets.exceptions import ConnectionClosedOK


async def handler(websocket, path):
    try:
        while 1:
            message = await websocket.recv()
            print('[+] ' + message)
            if message.startswith('DOMAIN--'):
                domain = message.split('|')[0][8:]
                password = message.split('|')[1][10:]
                loginPassword = get_login_password(domain, password)
                await websocket.send(loginPassword)
    except ConnectionClosedOK:
        print("[+] A connection has closed!!!")

def start():
    try:
        start_server = websockets.serve(handler, "127.0.0.1", 8765)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except OSError:
        print("[-] 127.0.0.1:8765 already in use!")

start()