import asyncio

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

if __name__ == '__main__':
    web.run_app(app)
