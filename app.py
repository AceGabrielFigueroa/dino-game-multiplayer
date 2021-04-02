from threading import Lock
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Threading stuff
thread = None
thread_lock = Lock()

# Player data
players = {}

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("update")
def update(x, y):
    players[request.sid] = [x, y]

def server_tick():
    while True:
        socketio.sleep(1/60)
        socketio.emit('server event', json.dumps(players))

@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(server_tick)

    print(f"USER[{request.sid}] CONNECTED")
    players[request.sid] = [0, 0]

@socketio.event
def disconnect():
    print(f"USER[{request.sid}] DISCONNECTED")
    del players[request.sid]

if __name__ == '__main__':
    socketio.run(app)