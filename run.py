import time
from flask import Flask
from flask_socketio import SocketIO


from pymultiwii import MultiWii

app = Flask(__name__)
socketio = SocketIO(app)
app.board = MultiWii('/dev/ttyUSB0')

@socketio.on('message')
def handle__message(message):
	print(app.board.attitude)
	app.board.sendCMD(8,MultiWii.SET_RAW_RC,message)
	print(message)

@socketio.on('disarm')
def handle_disarm(message):
        app.board.disarm()
        print("Disarmed.")
        print(message)

@socketio.on('arm')
def handle_arm(message):
        app.board.arm()
        print("Board is armed now!")
        print(message)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80)
