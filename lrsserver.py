from cmath import log
import os
import coloredlogs
import logging
import asyncio
import socketio

from aiohttp import web

sio = socketio.AsyncServer(cors_allowed_origins=[
                           "*", "localhost", "127.0.0.1"])
app = web.Application()
sio.attach(app)

coloredlogs.install()
logging.basicConfig(level=logging.INFO)


@sio.event
def connect(sid, environ, auth):
    logging.info(f"LRS_SERVER:CONNECT - SID[{sid}] - ALLOWED")


@sio.event
async def disconnect(sid):
    logging.info(f"LRS_SERVER:DISCONNECT - SID[{sid}] - DISCONNECTED")


@sio.event
async def login(*args, **kwargs):
    sid, data = args
    response = {"data": data, "error": None}

    try:
        sio.enter_room(sid, data["room"])
        logging.info(
            f"LRS_SERVER:LOGIN - [{sid}] entered to [{data['room']}]")
    except Exception as e:
        logging.info(
            f"LRS_SERVER:LOGIN - [{sid}] not entered to [{data['room']}]")
        response["error"] = str(e)

    await sio.emit("login_resp", response, to=sid)


@sio.event
async def logout(*args, **kwargs):
    sid, data = args
    response = {"data": data, "error": None}

    try:
        sio.leave_room(sid, data["room"])
        logging.info(
            f"LRS_SERVER:LOGOUT - SID[{sid}] from {data['room']} - ALLOWED")
    except Exception as e:
        logging.info(f"LRS_SERVER:LOGOUT - SID[{sid}] - DENIED")
        response["error"] = str(e)

    await sio.emit("logout_resp", response, to=sid)


@sio.event
async def ping(*args, **kwargs):
    sid, data = args
    logging.info(
        f"LRS_SERVER:PING:{data['method']}:{data['endpoint']} - [{sid}] to [{data['room']}]")
    await sio.emit("ping", data, room=data["room"], skip_sid=sid)


@sio.event
async def ping_resp(*args, **kwargs):
    sid, data = args
    response = {**data}
    print(response)
    await sio.emit("ping_resp", response, room=data["room"], skip_sid=sid)


@sio.event
async def subscribe(*args, **kwargs):
    sid, data = args
    logging.info(f"LRS_SERVER:SUBSCRIBE - SID[{sid}] - {data}")
    print("YAYYYY", data.keys())
    await sio.emit("subscribe", data, room=data["room"], skip_sid=sid)


@sio.event
async def subscribe_resp(*args, **kwargs):
    sid, data = args
    print(data)
    await sio.emit("subscribe_resp", data, room=data["room"], skip_sid=sid)


@sio.event
async def unsubscribe(*args, **kwargs):
    sid, data = args
    logging.info(f"LRS_SERVER:UNSUBSCRIBE - SID[{sid}] - {data}")
    print("YAYYYY", data.keys())
    await sio.emit("unsubscribe", data, room=data["room"], skip_sid=sid)


@sio.event
async def unsubscribe_resp(*args, **kwargs):
    sid, data = args
    await sio.emit("unsubscribe_resp", data, room=data["room"], skip_sid=sid)


if __name__ == "__main__":
    web.run_app(app, port=os.environ["PORT"])
