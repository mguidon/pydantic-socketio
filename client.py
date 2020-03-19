import socketio
from validator import validate
from model.model import MouseInput


sio = socketio.Client()


def send_mouse_input(valid: bool):
    data = { "button": 0, "delta" : 100, "modifiers" : 1, "pos" : { "x": 1, "y": 2}, "type" : "up" if valid else "wrong" }
    sio.emit("mouse_input", data)

def err(msg: str):
    print("Error handler")

@sio.event
def error(data):
    print(f"Error from server: {data}")

@validate(MouseInput, err)
def dummy_handler(data: MouseInput):
    print(f"data {data}")
    print(f"{type(data)}")

sio.on('dummy', dummy_handler)

@sio.event
def connect():
    print('connection established')
    send_mouse_input(True)
    send_mouse_input(False)
   
@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:8080')
sio.wait()