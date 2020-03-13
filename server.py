import io
from typing import Optional

import socketio
from aiohttp import web

import aiologger


sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

log = logging.getLogger(name=__name__)
log.setLevel(logging.INFO)

@sio.event
async def on_data(sid, data):
    log.debug(f"data coming in {data}")

@sio.event
async def on_connect(sid, environ):
    log.debug(f'connect {sid}')

@sio.event
async def disconnect(sid):
    print(sid, type(sid))
    log.debug(f'disconnect {sid}')

if __name__ == '__main__':
    web.run_app(app)
