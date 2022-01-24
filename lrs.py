from ast import match_case
import asyncio
from re import I
import signal
import os

import websockets

import protocols


lrc_clients = []
lra_clients = []
sessions = []


async def echo(websocket):
    async for message in websocket:
        protocol, data = message.split(":")

        match protocol:
            case "LRC_LOGIN":
                response = await protocols.LRC_LOGIN(websocket=websocket)
                await websocket.send(response)

            case "LRA_LOGIN":
                response = await protocols.LRA_LOGIN(websocket=websocket)
                await websocket.send(response)

            case "LRA_SET_SESSION":
                response = await protocols.LRA_SET_SESSION(websocket=websocket, lrcid=data)
                await websocket.send(response)

            case "LRA_API_REQUEST":
                response = await protocols.LRA_API_REQUEST(websocket=websocket, event=data)
                await websocket.send(response)


async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(echo, host="", port=int(os.environ["PORT"])) as s:
        await stop


if __name__ == "__main__":
    asyncio.run(main())
