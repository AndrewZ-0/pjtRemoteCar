import eventlet
import socketio

server = socketio.Server(cors_allowed_origins = "http://0.0.0.0:10000")
app = socketio.WSGIApp(server)

@server.on("connect")
def connect(sid, environ):
    print(sid, "has connected")

@server.on("message")
def message(sid, data):
    print(sid, "::", data)
    server.emit("message", data, room = sid)

if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 10000)), app)
