from encrypts import get_login_password
import asyncio
import websockets


async def handler(websocket, path):
    while 1:
        message = await websocket.recv()
        print(message)
        if message.startswith('DOMAIN--'):
            domain = message.split('|')[0][8:]
            password = message.split('|')[1][10:]
            loginPassword = get_login_password(domain, password)
            await websocket.send(loginPassword)

def start():
    start_server = websockets.serve(handler, "127.0.0.1", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


start()