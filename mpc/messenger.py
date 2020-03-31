from p2p import connect_and_send
from shamir import serialize_mul_msg, serialize_triple_ab_msg, serialize_triple_c_msg, deserialize_mul_msg, deserialize_triple_ab_msg, deserialize_triple_c_msg
from multiprocessing import Process
import json, os

class MockMessenger:

	def __init__(self, t, n, index, queues, uuid):
		self.t = t
		self.n = n
		self.queues = queues
		self.index = index
		self.uuid = uuid

	def broadcast(self, msg_type, round_n, data):
		for i in range(len(self.queues)):
			if i != self.index-1:
				self.queues[i].put((self.uuid, msg_type, round_n, data))

	def send(self, player, msg_type, round_n, data):
		self.queues[player-1].put((self.uuid, msg_type, round_n, data))

	def collect(self, round_n, full_quorum=False):
		out = []
		recv = self.queues[self.index-1]
		n_resps = self.t
		if full_quorum:
			n_resps = self.n-1
		while len(out) < n_resps:
			if not recv.empty():
				r = recv.get()
				if (self.uuid==r[0]) and (r[2] == round_n):
					out.append(r[3])
				elif (self.uuid==r[0]) and (r[2] < round_n):
					pass
				else:
					recv.put(r)
		return out

class Messenger:

	def __init__(self, t, n, index, directory, idx2peer, uuid):
		self.t = t
		self.n = n
		self.dir = directory
		self.index = index
		self.uuid = uuid
		self.idx2peer = idx2peer

	def broadcast(self, msg_type, round_n, data):
		for k, v in self.idx2peer.items():
			if k != self.index:
				self.send(k, msg_type, round_n, data)

	def send(self, player_idx, msg_type, round_n, data):
		peer = self.idx2peer[player_idx]
		if msg_type == "MUL":
			data = serialize_mul_msg(data)
		elif msg_type == "TRIP-AB":
			data = serialize_triple_ab_msg(data)
		elif msg_type == "TRIP-C":
			data = serialize_triple_c_msg(data)		
		msg = {'uuid': self.uuid, 'sender': self.index, 'round': round_n, 'msgtype': msg_type, 'data': data}
		p = Process(target=connect_and_send, args=(json.dumps(msg), peer[0], peer[1]))
		p.start()
		p.join()
		print("msg sent...")

	def collect(self, round_n, full_quorum=False):
		out = []
		n_resps = self.t
		if full_quorum:
			n_resps = self.n-1
		fnames = [os.path.join(self.dir, f"{self.uuid}_{i}_{round_n}") for i in range(1, self.n+1) if i!=self.index]
		while len(out) < n_resps:
			for file in fnames:
				if os.path.isfile(file):
					print("msg received...")
					with open(file, "r") as f:
						data = f.read()
					msg = json.loads(data)
					if msg['msgtype'] == "MUL":
						data = deserialize_mul_msg(msg['data'])
					elif msg['msgtype'] == "TRIP-AB":
						data = deserialize_triple_ab_msg(msg['data'])
					elif msg['msgtype'] == "TRIP-C":
						data = deserialize_triple_c_msg(msg['data'])
					else:
						data = msg['data']
					out.append(data)
					fnames.remove(file)
					break
		return out