import eventlet
import socketio

class RaspiSioServer:
    def __init__(self):
        self.commandsStack = []
        
        self.server = socketio.Server(cors_allowed_origins = "*")
        self.app = socketio.WSGIApp(self.server)
        self.client_addr = (None, None)

        self.setupEventHandlers()
        
    def setupEventHandlers(self):
        @self.server.on("connect")
        def connect(sid, environ):
            self.setClientData(environ)
            print("[CONNECTION]")
            print(self.client_addr, "has connected on port", self.client_port)

        @self.server.on("message")
        def message(sid, dataPackage):
            print(f">>>({self.client_addr})({self.client_port}) :: {dataPackage}")
            self.commandsStack.append(dataPackage)

        @self.server.on("disconnect")
        def disconnect(sid):
            print("[DISCONNECTION]")
            print(self.client_addr, "has disconnected from port", self.client_port)
            self.setClientData(None)
            print("\nWaiting for connection...\n")
    
    def setClientData(self, environ):
        if environ is not None:
            self.client_addr = environ["REMOTE_ADDR"]
            self.client_port = environ["REMOTE_PORT"]
        else:
            self.client_addr = None
            self.client_port = None
        
    def start(self):
        server_addr = ("0.0.0.0", 10000)

        print("[SERVER OPEN]")
        print("----------------------------------------------------------")
        print("\nWaiting for connection...\n")

        listener = eventlet.listen(server_addr)
        eventlet.wsgi.server(listener, self.app, log_output = False)
    

if __name__ == "__main__":
    rss = RaspiSioServer()
    rss.start()


