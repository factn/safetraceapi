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

	def collect(self, round_n):
		out = []
		recv = self.queues[self.index-1]
		while len(out) < self.t+1:
			if not recv.empty():
				r = recv.get()
				if r[0] == round_n:
					out.append(r[1])
				else:
					recv.put(r)
		# print(f"{self.index} collected enough messages for round {round_n}")
		return out
