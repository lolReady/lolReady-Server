from cmath import log
import os
from pprint import pprint
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
    logging.info(f"LRS_SERVER<CONNECT> - {sid} - ALLOWED")


@sio.event
async def disconnect(sid):
    print("DISCONNECTED", sid)
    logging.info(f"LRS_SERVER<DISCONNECT> - {sid} - DISCONNECTED")


@sio.event
async def login(sid, payload):
    response = {**payload, "error": None}

    try:
        sio.enter_room(sid, payload["room"])
        logging.info(
            f"LRS_SERVER<LOGIN> - [{sid}] entered to [{payload['room']}]")
    except Exception as e:
        logging.info(
            f"LRS_SERVER:LOGIN - [{sid}] not entered to [{response['room']}]")
        response["error"] = str(e)

    await sio.emit("login_resp", response, to=sid)


@sio.event
async def logout(sid, payload):
    response = {**payload, "error": None}

    try:
        sio.leave_room(sid, payload["room"])
        logging.info(
            f"LRS_SERVER<LOGOUT> - {sid} from {payload['room']} - ALLOWED")
    except Exception as e:
        logging.info(f"LRS_SERVER<LOGOUT> - {sid} - DENIED")
        response["error"] = str(e)

    await sio.emit("logout_resp", response, to=sid)


@sio.event
async def ping(sid, payload):
    logging.info(f"LRS_SERVER<PING> - {sid}")
    await sio.emit("ping", payload, room=payload["room"], skip_sid=sid)


@sio.event
async def ping_resp(sid, payload):
    logging.info(f"LRS_SERVER<PING_RESP> - {sid}")
    await sio.emit("ping_resp", payload, room=payload["room"], skip_sid=sid)


@sio.event
async def subscribe(sid, payload):
    logging.info(f"LRS_SERVER<SUBSCRIBE> - {sid}")
    await sio.emit("subscribe", payload, room=payload["room"], skip_sid=sid)


@sio.event
async def subscribe_resp(sid, payload):
    logging.info(f"LRS_SERVER<SUBSCRIBE_RESP> - {sid}")
    await sio.emit("subscribe_resp", payload, room=payload["room"], skip_sid=sid)


@sio.event
async def unsubscribe(sid, payload):
    logging.info(f"LRS_SERVER<UNSUBSCRIBE> - {sid}")
    await sio.emit("unsubscribe", payload, room=payload["room"], skip_sid=sid)


@sio.event
async def unsubscribe_resp(sid, payload):
    logging.info(f"LRS_SERVER<UNSUBSCRIBE_RESP> - {sid}")
    await sio.emit("unsubscribe_resp", payload, room=payload["room"], skip_sid=sid)


if __name__ == "__main__":
    web.run_app(app, port=os.environ["PORT"])
