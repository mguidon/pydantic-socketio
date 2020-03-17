import io
from typing import Optional

import socketio
from aiohttp import web

import logging

from logging import getLogger

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

logger = getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(message)s")


@sio.event
async def mouseInput(sid, data):
    logger.debug(f"mouseInput {data}")

@sio.event
async def data(sid, data):
    logger.debug(f"data coming in {data}")

@sio.event
async def on_connect(sid, environ):
    logger.debug(f'connect {sid}')

@sio.event
async def disconnect(sid):
    logger.debug(f'disconnect {sid}')

if __name__ == '__main__':
    web.run_app(app)
