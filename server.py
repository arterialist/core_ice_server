import argparse

from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer

from models.peers import Client

peers = dict()


class SignalingServer(WebSocket):
    def handleClose(self):
        if is_debug:
            print("handleClose")
        address = (self.address[0], self.address[1])
        peers.pop(address, None)
        print(f"Client {self.address[0]}:{self.address[1]} disconnected")

    def handleMessage(self):
        if is_debug:
            print("handleMessage")
        print(f"New Message: {self.data}")
        address = (self.address[0], self.address[1])
        if is_interactive:
            response = input()
        else:
            response = self.data

        for peer_address in peers:
            if peer_address != address:
                peers.get(peer_address)["socket"].sendMessage(response)

    def handleConnected(self):
        if is_debug:
            print("handleConnected")
        address = (self.address[0], self.address[1])
        peer = Client(self.address[0], self.address[1])
        peers[address] = {
            "peer": peer,
            "socket": self
        }
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
