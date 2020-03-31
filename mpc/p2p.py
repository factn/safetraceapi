from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import connectProtocol, TCP4ClientEndpoint
from twisted.internet import reactor
import json, os

class MPCListener(Protocol):
    
    def __init__(self, directory):
        self.dir = directory
        self.current_recv = b''
        self.peer = None
    
    def dataReceived(self, data):
        self.current_recv += data
        if data.decode()[-1] != '\n':
            return
        else:
            print("receiving msg...")
            line = self.current_recv.strip()
            self.current_recv = b''
            msg = json.loads(line)
            fname = f"{msg['uuid']}_{msg['sender']}_{msg['round']}"
            temppath = os.path.join(self.dir, fname+"_t")
            with open(temppath, "w") as f:
                f.write(line.decode())
            os.rename(temppath, os.path.join(self.dir, fname))
            self.transport.loseConnection()

    def connectionMade(self):
        peer = self.transport.getPeer()
        self.peer = peer.host+":"+str(peer.port)
        print("Connection from", self.peer)

    def connectionLost(self, reason):
        print(self.peer, "disconnected")

class MPCFactory(Factory):

    protocol = MPCListener

    def __init__(self, directory):
        self.dir = directory

    def buildProtocol(self, *args, **kwargs):
        protocol = MPCListener(self.dir)
        return protocol

def run_mpc_listener(directory, my_port):
    f = MPCFactory(directory)
    reactor.listenTCP(my_port, f)
    reactor.run()

class MPCSender(Protocol):

    def __init__(self, msg):
        self.msg = msg

    def connectionMade(self):
        peer = self.transport.getPeer()
        self.peer = peer.host+":"+str(peer.port)
        print("Connected to", self.peer)
        print("sending msg...")
        msg = self.msg + "\n"
        self.transport.write(str.encode(msg))

    def connectionLost(self, reason):
        print(self.peer, "disconnected")
        reactor.stop()

def connect_and_send(msg, connect_host, connect_port):
    point = TCP4ClientEndpoint(reactor, connect_host, connect_port)
    d = connectProtocol(point, MPCSender(msg))
    reactor.run()


