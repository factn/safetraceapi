from shamir import Shamir
from serialize import *
import asyncio, json

class Client:

	def __init__(self, t, n, idx2node):
		self.t = t
		self.n = n
		self.idx2node = idx2node

	def send_operation(self, val, uuid):
		return asyncio.run(self.operation(val, uuid))

	async def operation(self, val, uuid):
		procs = []
		msg = {'uuid': uuid}
		bv = bin(val)[2:]
		while len(bv) < 64:
			bv = '0' + bv
		shares = Shamir(self.t, self.n).share_bitstring_secret(bv[::-1])
		tasks = []
		for k, v in self.idx2node.items():
			msg = {'uuid': uuid, 'inputs': serialize_shares(shares[k-1])}
			host, port = v
			tasks.append(talk_to_single_server(msg, host, port))
		msgs = await asyncio.gather(*tasks)
		vals = [deserialize_shares(msg['result']) for msg in msgs if msg != None]
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
