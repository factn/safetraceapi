from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import connectProtocol, TCP4ClientEndpoint
from twisted.internet import reactor
from shamir import serialize_mul_msg, serialize_triple_ab_msg, serialize_triple_c_msg, deserialize_mul_msg, deserialize_triple_ab_msg, deserialize_triple_c_msg
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
            if msg['msgtype'] == "MUL":
                data = deserialize_mul_msg(msg['data'])
            elif msg['msgtype'] == "TRIP-AB":
                data = deserialize_triple_ab_msg(msg['data'])
            elif msg['msgtype'] == "TRIP-C":
                data = deserialize_triple_c_msg(msg['data'])
            else:
                return
            self.recv_queue.put((msg['uuid'], msg['msgtype'], msg['round'], msg['data']))

    def connectionMade(self):
        peer = self.transport.getPeer()
        self.peer = peer.host+":"+str(peer.port)
        print("Connection from", self.peer)

    def connectionLost(self, reason):
        print(self.peer, "disconnected")

class ClientMPC(Protocol):

    def __init__(self, queue):
        self.send_queue = queue
        self.current_recv = b''
        self.peer = None

    def connectionMade(self):
        peer = self.transport.getPeer()
        self.peer = peer.host+":"+str(peer.port)
        print("Connected to", self.peer)
        while True:
            if not self.send_queue.empty():
                msg = self.send_queue.get()
                if msg == "STOP":
                    self.transport.loseConnection()
                    reactor.stop()
                if msg[1] == "MUL":
                    data = serialize_mul_msg(msg[3])
                elif msg[1] == "TRIP-AB":
                    data = serialize_triple_ab_msg(msg[3])
                elif msg[1] == "TRIP-C":
                    data = serialize_triple_c_msg(msg[3])
                else:
                    continue
                m = {'uuid': msg[0], 'msgtype': msg[1], 'round': msg[2], 'data': msg[3]}
                m = json.dumps(m)
                m = m + "\n"
                self.transport.write(str.encode(m))

    def connectionLost(self, reason):
        print(self.peer, "disconnected")
        reactor.stop()

class ServerFactory(Factory):

    protocol = ServerMPC

    def __init__(self, queue):
        self.queue = queue

    def buildProtocol(self, *args, **kwargs):
        protocol = ServerMPC(self.queue)
        return protocol

def runserver(queue, my_port):
    f = ServerFactory(queue)
    reactor.listenTCP(my_port, f)
    reactor.run()

def runclient(queue, connect_host, connect_port):
    point = TCP4ClientEndpoint(reactor, connect_host, connect_port)
    d = connectProtocol(point, ClientMPC(queue))
    reactor.run()