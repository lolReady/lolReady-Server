import os
import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)


lrcs = []


@sio.event
def connect(sid, environ, auth):
    lrcs.append(sid)
    print("Connected ", sid, environ, auth)


@sio.event
def login(sid, data):
    print("LOGIN", sid, data)


@sio.event
def disconnect(sid):
    print("Disconnected ", sid)


@sio.event
def forward(sid):
    pass


if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(('', os.environ["PORT"])), app)
