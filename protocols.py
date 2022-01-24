from re import A
import lrs


async def LRC_LOGIN(*args, **kwargs):
    websocket = kwargs["websocket"]

    if websocket not in lrs.lrc_clients:
        lrs.lrc_clients.append(websocket)
        return f"LRC_LOGIN:{websocket.id} is succesfull"
    else:
        return f"LRC_LOGIN:{websocket.id} is already defined"


async def LRA_LOGIN(*args, **kwargs):
    websocket = kwargs["websocket"]

    if websocket not in lrs.lra_clients:
        lrs.lra_clients.append(websocket)
        return f"LRA_LOGIN:{websocket.id} is succesfull"
    else:
        return f"LRA_LOGIN:{websocket.id} is already defined"


async def LRA_SET_SESSION(*args, **kwargs):
    websocket = kwargs["websocket"]
    lrcid = kwargs["lrcid"]

    for lrcc in lrs.lrc_clients:
        if str(lrcc.id) == lrcid:
            lrs.sessions.append([lrcid, str(websocket.id)])
            return f"LRA_SET_SESSION:{websocket.id}~{lrcid} were paired"

    return f"LRA_SET_SESSION:{websocket.id}~{lrcid} were not paired"


async def LRC_SET_SESSION(*args, **kwargs):
    pass


async def LRA_GET_SESSION(*args, **kwargs):
    pass


async def LRC_GET_SESSION(*args, **kwargs):
    pass


async def LRC_CLOSE_SESSION(*args, **kwargs):
    pass


async def LRA_CLOSE_SESSION(*args, **kwargs):
    pass


async def LRA_API_REQUEST(*args, **kwargs):
    websocket = kwargs["websocket"]  # lra
    event = kwargs["event"]  # event
    error = False
    lrcid = None

    for paired in lrs.sessions:
        if paired[1] == str(websocket.id):
            lrcid = paired[0]
            break
        error = True

    lrc = None
    if lrcid:
        for lrcc in lrs.lrc_clients:
            if str(lrcc.id) == lrcid:
                lrc = lrcc
            else:
                error = True

    if lrc:
        await lrc.send(f"API_REQUEST ALLOWED WITH {event}")
    else:
        error = True

    if error:
        return "ERROR"

    return "DONE"


__all__ = [
    LRC_LOGIN, LRA_LOGIN,
    LRC_SET_SESSION, LRA_SET_SESSION,
    LRC_GET_SESSION, LRA_GET_SESSION,
    LRC_CLOSE_SESSION, LRA_CLOSE_SESSION,
    LRA_API_REQUEST,
]
