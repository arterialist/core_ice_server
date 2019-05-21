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
        address = (self.address[0], self.address[1])
        print(f"New Message from {address[0]}{address[1]}: {self.data}")

        if address not in peers:
            return

        if is_interactive:
            response = input()
        else:
            response = self.data

        for peer_address in peers:
            if peer_address != address:
                peers.get(peer_address)["socket"].sendMessage(response)
                if is_relay:
                    break

    def handleConnected(self):
        if is_debug:
            print("handleConnected")
        if len(peers) == 2 and is_relay:
            return
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
parser.add_argument('--relay', help="Act as relay", action="store_true")
parser.add_argument('--interactive', help="Enable interactive response", action="store_true")

args = parser.parse_args()
port = args.port
is_debug = args.debug
is_relay = args.relay
is_interactive = args.interactive

server = SimpleWebSocketServer('', port, SignalingServer)
server.serveforever()
