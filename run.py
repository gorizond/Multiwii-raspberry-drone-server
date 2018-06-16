import asyncio
import time
from aiohttp import web

import socketio

from pymultiwii import MultiWii

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)
app.board = MultiWii('/dev/ttyUSB0')
app.board.connect()

@sio.on('message', namespace='/test')
async def test_message(sid, message):
    print(app.board.attitude)
    app.board.sendCMD(8,MultiWii.SET_RAW_RC,message)
    print(message)

@sio.on('disconnect request', namespace='/test')
async def disconnect_request(sid):
    await sio.disconnect(sid, namespace='/test')


@sio.on('connect', namespace='/test')
async def test_connect(sid, environ):
    print('Client connect')


@sio.on('disconnect', namespace='/test')
def test_disconnect(sid):
    print('Client disconnected')


async def index(request):
    return web.json_response(app.board.getData(MultiWii.ATTITUDE))

async def send(request):
    cmd = int(request.match_info.get('cmd', MultiWii.ATTITUDE))
    data = [int(i) for i in request.match_info.get('data', "").split(",")]
    size = int(request.match_info.get('size', 0))
    app.board.sendCMD(size, cmd, data)
    return web.json_response({"cmd":cmd, "data":data, "size":size})

async def arm(request):
    timer = 0
    start = time.time()
    while timer < 0.5:
        data = [1500,1500,2000,1000]
        app.board.sendCMD(8,MultiWii.SET_RAW_RC,data)
        await asyncio.sleep(0.05)
        timer = timer + (time.time() - start)
        start =  time.time()
    return web.json_response({"status":"arm"})

async def disarm(request):
    timer = 0
    start = time.time()
    while timer < 0.5:
        data = [1500,1500,1000,1000]
        app.board.sendCMD(8,MultiWii.SET_RAW_RC,data)
        await asyncio.sleep(0.05)
        timer = timer + (time.time() - start)
        start =  time.time()
    return web.json_response({"status":"disarm"})


app.router.add_get('/', index)
app.router.add_get('/send/{cmd}/{data}/{size}', send)
app.router.add_get('/arm', arm)
app.router.add_get('/disarm', disarm)


if __name__ == '__main__':
    web.run_app(app)
