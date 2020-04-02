from serialize import *

class Messenger:

	def __init__(self, t, n, index, queues, uuid):
		self.t = t
		self.n = n
		self.queues = queues
		self.index = index
		self.uuid = uuid

	def broadcast(self, msg_type, round_n, data):
		for i in range(1, self.n+1):
			if i != self.index:
				self.send(i, msg_type, round_n, data)

	def send(self, player, msg_type, round_n, data):
		if msg_type == "MUL":
			b = serialize_mul_msg(data)
		elif msg_type == "TRIP-AB":
			b = serialize_triple_ab_msg(data)
		elif msg_type == "TRIP-C":
			b = serialize_triple_c_msg(data)
		else:
			raise ValueError(f"Unknown msg type: {msg_type}")
		self.queues[player-1].put({'uuid': self.uuid, 'msgtype': msg_type, 'round': round_n, 'data': b})

	def collect(self, round_n, full_quorum=False):
		out = []
		recv = self.queues[self.index-1]
		n_resps = self.t
		if full_quorum:
			n_resps = self.n-1
		while len(out) < n_resps:
			if not recv.empty():
				r = recv.get()
				if (self.uuid==r['uuid']) and (r['round'] == round_n):
					if r['msgtype'] == "MUL":
						data = deserialize_mul_msg(r['data'])
					elif r['msgtype'] == "TRIP-AB":
						data = deserialize_triple_ab_msg(r['data'])
					elif r['msgtype'] == "TRIP-C":
						data = deserialize_triple_c_msg(r['data'])
					else:
						raise ValueError(f"Unknown msg type: {r['msgtype']}")
					out.append(data)
				elif (self.uuid==r['uuid']) and (r['round'] < round_n):
					pass
				else:
					recv.put(r)
		return out
