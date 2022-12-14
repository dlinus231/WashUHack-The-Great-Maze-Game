from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from GenerateMaze import generateEdges
import MPU6050 
import time


app = Flask(__name__)
socketio = SocketIO(app)


mpu = MPU6050.MPU6050()
accel = [0]*3


def setup():
    mpu.dmp_initialize()


@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/game')
def home():
    return render_template('game.html')

@app.route('/winner')
def winner():
    return render_template('winner.html')

@app.route('/loser')
def loser():
    return render_template('loser.html')


@socketio.on('start game')
def start_game(start):
    if(start == 1):
        emit('edges_data', generateEdges())
        while(True):
            accel = mpu.get_acceleration()
            for i in range(len(accel)):
                accel[i] /= 16384.0
            emit('accel_data', accel)
            time.sleep(1/60)


if __name__ == '__main__':
    setup()
    socketio.run(app, debug=True, port=80, host='0.0.0.0')
