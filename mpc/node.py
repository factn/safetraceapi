from p2p import run_mpc_listener
from multiprocessing import Process
from messenger import Messenger
from triples import TripleGeneration
from circuit import Circuit
from shamir import Shamir, Share

class MPCNode:

	def __init__(self, t, n, index, port, directory, idx2peer):
		self.t = t
		self.n = n
		self.idx2peer = idx2peer
		self.index = index
		self.port = port
		self.dir = directory
		self.server = Process(target=run_mpc_listener, args=(self.dir, self.port))

	def start(self):
		self.server.start()

	def stop(self):
		self.server.terminate()

	def run_triples_protocol(self, uuid, batch_size, n_batches):
		m = Messenger(self.t, self.n, self.index, self.dir, self.idx2peer, uuid)
		s = Shamir(self.t, self.n)
		t = TripleGeneration(self.index, s, m, batch_size=batch_size, n_batches=n_batches)
		t.run()
		return t.triples

	def run_circuit_protocol(self, uuid, path, inputs, triples):
		m = Messenger(self.t, self.n, self.index, self.dir, self.idx2peer, uuid)
		s = Shamir(self.t, self.n)
		itypes = []
		for i in inputs:
			if i in [0,1]:
				itypes.append('V')
			elif type(i) == Share:
				itypes.append('S')
			else:
				raise ValueError("bad inputs")
		c = Circuit(path, itypes)
		return c.evaluate(inputs, shamir=s, messenger=m, triples=triples)
