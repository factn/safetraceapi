class Messenger:

	def __init__(self, t, n, index, queues, uuid):
		self.t = t
		self.n = n
		self.queues = queues
		self.index = index
		self.uuid = uuid

	def broadcast(self, msg_type, round_n, data):
		for i in range(len(self.queues)):
			if i != self.index-1:
				self.queues[i].put((uuid, msg_type, round_n, data))

	def send(self, player, msg_type, round_n, data):
		self.queues[player-1].put((uuid, msg_type, round_n, data))

	def collect(self, msg_type, round_n, full_quorum=False):
		out = []
		recv = self.queues[self.index-1]
		n_resps = self.t
		if full_quorum:
			n_resps = self.n-1
		while len(out) < n_resps:
			if not recv.empty():
				r = recv.get()
				if (self.uuid==r[0]) and (r[2] == round_n):
					out.append(r[1])
				elif (self.uuid==r[0]) and (r[2] < round_n):
					pass
				else:
					recv.put(r)
		return out
