from multiprocessing import Queue, Process

class MockMessenger:

	def __init__(self, t, n, index, queues):
		self.t = t
		self.n = n
		self.queues = queues
		self.index = index

	def broadcast(self, round_n, data):
		# print(f"{self.index} broadcasting message for round {round_n}")
		for i in range(len(self.queues)):
			if i != self.index-1:
				self.queues[i].put((round_n, data))

	def send(self, player, round_n, data):
		self.queues[player-1].put((round_n, data))

	def collect(self, round_n, full_quorum=False):
		out = []
		recv = self.queues[self.index-1]
		n_resps = self.t
		if full_quorum:
			n_resps = self.n-1
		while len(out) < n_resps:
			if not recv.empty():
				r = recv.get()
				if r[0] == round_n:
					out.append(r[1])
				elif r[0] > round_n:
					recv.put(r)
		# print(f"{self.index} collected enough messages for round {round_n}")
		return out
