from flask import Flask, render_template, request
from flask_socketio import SocketIO
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

players = {}

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on('connect')
def onConnect():
    print("USER CONNECTED")
    print(request.sid)
    players[request.sid] = [0, 0]
    socketio.emit("update", json.dumps(players))

@socketio.on('disconnect')
def onDisconnect():
    print("USER DISCONNECTED")
    print(request.sid)
    del players[request.sid]
    print(players)
    socketio.emit("update", json.dumps(players))

@socketio.on("update")
def update(x, y):
    players[request.sid] = [x, y]
    socketio.emit("update", json.dumps(players))

if __name__ == '__main__':
    socketio.run(app)