import argparse

from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer


class SignalingServer(WebSocket):
    def handleClose(self):
        if is_debug:
            print("handleClose")
        print(f"Client {self.address[0]}:{self.address[1]} disconnected")

    def handleMessage(self):
        if is_debug:
            print("handleMessage")
        print(f"New Message: {self.data}")
        if is_interactive:
            response = input("Response: ")
            self.sendMessage(response)
        else:
            self.sendMessage(f"Echo: {self.data}")

    def handleConnected(self):
        if is_debug:
            print("handleConnected")
        print(f"Client {self.address[0]}:{self.address[1]} connected")

    def send(self, data):
        self.sendMessage(str(data))


parser = argparse.ArgumentParser(description="Server Parameters")
parser.add_argument('--port', type=int, default=4096, help="Server listening port")
parser.add_argument('--debug', help="Enable debug logs", action="store_true")
parser.add_argument('--interactive', help="Enable interactive response", action="store_true")

args = parser.parse_args()
port = args.port
is_debug = args.debug
is_interactive = args.interactive

server = SimpleWebSocketServer('', port, SignalingServer)
server.serveforever()
