from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import connectProtocol, TCP4ClientEndpoint
from twisted.internet import reactor
from shamir import 
import json

class ServerMPC(Protocol):
    
    def __init__(self, queue):
        self.recv_queue = queue
        self.current_recv = b''
        self.peer = None
    
    def dataReceived(self, data):
        self.current_recv += data
        if data.decode()[-1] != '\n':
            return
        else:
            line = self.current_recv.strip()
            self.current_recv = b''
            msg = json.loads(line)
            msg['round'], deserialize_round_msg(msg['data']) 

    def connectionMade(self):
        peer = self.transport.getPeer()
        self.peer = peer.host+":"+str(peer.port)
        print("Connection from", self.peer)

    def connectionLost(self, reason):
        print(self.peer, "disconnected")

class ClientMPC(Protocol):

    def connectionMade(self):
        peer = self.transport.getPeer()
        print("Connected to", peer.host+":"+str(peer.port))
        msg = {'msgtype': 'hello', 'content': 'hello there server!'}
        hello = json.dumps(msg)
        hello = hello + "\n"
        self.transport.write(str.encode(hello))

class MockMPCFactory(Factory):

    protocol = MockMPC

    def __init__(self, n_nodes):
        self.n_nodes = n_nodes

    def buildProtocol(self, *args, **kwargs):
        protocol = MockMPC(self.n_nodes)
        return protocol

def runserver(n_nodes, my_port):
    f = MockMPCFactory(n_nodes)
    reactor.listenTCP(my_port, f)
    reactor.run()

def runclient(connect_host, connect_port):
    point = TCP4ClientEndpoint(reactor, connect_host, connect_port)
    d = connectProtocol(point, MockMPCClient())
    reactor.run()