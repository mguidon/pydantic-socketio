import io
import logging
from logging import getLogger
from typing import Optional

import socketio
from aiohttp import web

from model.model import MouseInput
from validator import validate_asyn, register_validate_asyn

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

logger = getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(message)s")

async def on_error(sid, msg: str):
    logger.error(f"{msg}")
    await sio.emit("error", msg, room=sid)

@validate_asyn(cls=MouseInput, err_callback=on_error)
async def mouse_input(sid, data: MouseInput):
    logger.debug(f"mouse_input: sid: {sid} {type(data)}: {data}")
    data = { "button": 0, "delta" : 100, "modifiers" : 1, "pos" : { "x": 1, "y": 2}, "type" : "up"}
    await sio.emit("dummy", data, room=sid)

sio.on('mouse_input', mouse_input)

@sio.event
async def connect(sid, environ):
    logger.debug(f'connect {sid}')
    data = { "button": 0, "delta" : 100, "modifiers" : 1, "pos" : { "x": 1, "y": 2}, "type" : "up"}
    mouse_input_data = MouseInput(**data)
    await sio.emit("dummy", mouse_input_data.dict(), room=sid)

@sio.event
async def disconnect(sid):
    logger.debug(f'disconnect {sid}')

if __name__ == '__main__':
    web.run_app(app)
