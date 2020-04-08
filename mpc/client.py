from shamir import Shamir
from serialize import *
import asyncio, json

CLIENT_TIMEOUT = 600

class Client:

	def __init__(self, t, n, idx2node):
		self.t = t
		self.n = n
		self.idx2node = idx2node

	def send_operation(self, x, y, uuid):
		return asyncio.run(self.operation(x, y, uuid))

	async def operation(self, x, y, uuid):
		bx = bin(x)[2:]
		while len(bx) < 31:
			bx = '0' + bx
		x_shares = Shamir(self.t, self.n).share_bitstring_secret(bx[::-1])
		by = bin(y)[2:]
		while len(by) < 31:
			by = '0' + by	
		y_shares = Shamir(self.t, self.n).share_bitstring_secret(by[::-1])
		tasks = []
		for k, v in self.idx2node.items():
			msg = {'uuid': uuid, 'x_inputs': serialize_shares(x_shares[k-1]), 'y_inputs': serialize_shares(y_shares[k-1])}
			host, port = v
			tasks.append(talk_to_single_server(msg, host, port))
		vals = []
		for res in asyncio.as_completed(tasks, timeout=CLIENT_TIMEOUT):
			msg = await res
			if msg != None:
				vals.append(deserialize_shares(msg['result']))
			if len(vals) > self.t:
				break
		return Shamir(self.t, self.n).reconstruct_bitstring_secret(vals)

async def talk_to_single_server(msg, host, port):
	reader, writer = await asyncio.open_connection(host, port)
	send = json.dumps(msg)
	writer.write(str.encode(send+'\n'))
	await writer.drain()
	try:
		data = await reader.readline()
		data = data.strip()
		msg = json.loads(data.decode())
		writer.close()
		return msg
	except:
		writer.close()
	return None
