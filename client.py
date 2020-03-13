import socketio

sio = socketio.Client()


def send_data():
    data = { '1' : 'one'}
    sio.emit("data", data)

@sio.event
def connect():
    print('connection established')
    send_data()

@sio.event
def log(data):
    print(data)

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:8080')
sio.wait()