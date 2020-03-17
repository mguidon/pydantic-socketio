import socketio

sio = socketio.Client()

def send_data():
    data = { '1' : 'one'}
    sio.emit("data", data)

def send_mouse_input():
    data = { '1' : 'one'}
    sio.emit("data", data)

@sio.event
def connect():
    print('connection established')
    send_mouse_input()
   
@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:8080')
sio.wait()