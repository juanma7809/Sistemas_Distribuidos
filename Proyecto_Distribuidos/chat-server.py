from flask import Flask, render_template
from flask_socketio import SocketIO
import persistance
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'abc123'
socketio = SocketIO(app, cors_allowed_origins='*')

@app.route("/chat")
def chat():
    return render_template('index.html')

@socketio.on('connected')
def connected(data):
    print(data)


@socketio.on("message")
def get_message(json, methods=['POST']):
    print("mensaje:" + str(json))
    socketio.emit("response", json)



if __name__ == "__main__":
    socketio.run(app)