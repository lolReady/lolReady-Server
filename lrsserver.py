import os
import coloredlogs
import logging
import asyncio
import socketio

from aiohttp import web

sio = socketio.AsyncServer(cors_allowed_origins=["*"])
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
    response = {**data, "error": None}

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
    response = {**data, "error": None}

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
        f"LRS_SERVER:PING:{data['method']}:{data['action']} - [{sid}] to [{data['room']}]")
    await sio.emit("ping", data, room=data["room"], skip_sid=sid)


@sio.event
async def ping_resp(*args, **kwargs):
    sid, data = args
    response = {**data}
    await sio.emit("ping_resp", response, room=data["room"], skip_sid=sid)


if __name__ == "__main__":
    web.run_app(app, port=os.environ["PORT"])
