from multiprocessing import Queue, Process
from shamir import Shamir
from serialize import *
import socket, select, json

class Client:

	def __init__(self, t, n, idx2node):
		self.t = t
		self.n = n
		self.idx2node = idx2node
		self.queue = Queue()

	def send_operation(self, val, uuid):
		procs = []
		msg = {'uuid': uuid}
		bv = bin(val)[2:]
		while len(bv) < 64:
			bv = '0' + bv
		shares = Shamir(self.t, self.n).share_bitstring_secret(bv[::-1])
		for k, v in self.idx2node.items():
			msg = {'uuid': uuid, 'inputs': serialize_shares(shares[k-1])}
			host, port = v
			procs.append(Process(target=run_single_client, args=(msg, host, port, self.queue)))
		for p in procs:
			p.start()
		for p in procs:
			p.join()
		vals = []
		while not self.queue.empty():
			msg = self.queue.get()
			vals.append(deserialize_shares(msg['result']))
		v = Shamir(self.t, self.n).reconstruct_bitstring_secret(vals)
		return v

def run_single_client(msg, host, port, queue):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	msg = json.dumps(msg)
	s.sendall(str.encode(msg+'\n'))
	data = s.recv(1024)
	while data.decode()[-1] != '\n':
		data += sock.recv(1024)
	data = data.strip()
	resp = json.loads(data.decode())
	queue.put(resp)
	s.close()
