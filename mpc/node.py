from p2p import runclient, runserver
from circuit import Circuit
from multiprocessing import Process, Queue
from triple_gen import TripleGeneration
from shamir import Shamir
from messenger import Messenger

class MPCNode:

	def __init__(self, t, n, port, idx2peer):
		self.t = t
		self.n = n
		self.shamir = Shamir(t, n)
		self.idx2peer = idx2peer
		self.index = None
		self.queues = [Queue() for _ in range(self.n)]
		self.server_process = None
		self.client_processes = []
		for k, v in self.idx2peer.items():
			if v == None:
				self.index = k
				self.server_process = Process(target=runserver, args=(self.queues[k-1], port))
			else:
				p = Process(target=runclient, args=(self.queues[k-1], v[0], v[1]))
				self.client_processes.append(p)				
		self.server_process.start()

	def start_clients(self):
		for p in self.client_processes:
			p.start()

	def stop_clients(self):
		for p in self.client_processes:
			p.terminate()

	def stop(self):
		self.server_process.terminate()
		for q in self.queues:
			q.close()
			q.join_thread()

	def run_triples_protocol(self, uuid, batch_size=10, n_batches=2):
		messenger = Messenger(t, n, self.index, self.queues, uuid)
		tg = TripleGeneration(self.index, self.shamir, messenger, batch_size=batch_size, n_batches=n_batches)
		tg.run()
		return tg.triples
