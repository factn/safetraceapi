from shamir import Shamir
from serialize import *
import asyncio, json, ssl, os

CLIENT_TIMEOUT = 600

class Client:

	def __init__(self, t, n, idx2node, certfile=None, keyfile=None, cafile=None):
		self.t = t
		self.n = n
		self.idx2node = idx2node
		self.certfile = certfile
		if self.certfile == None:
			self.certfile = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certs'), f'client-test.crt')
		self.keyfile = keyfile
		if self.keyfile == None:
			self.keyfile = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certs'), f'client-test.key')
		self.cafile = cafile
		if self.cafile == None:
			self.cafile = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certs'), 'testCA.pem')

	def do_intersection_operation(self, x, y, uuid):
		return asyncio.run(self.intersection_operation(x, y, uuid))

	async def intersection_operation(self, x, y, uuid):
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
			msg = {'msgtype': 'get-intersection', 'uuid': uuid, 'x_inputs': serialize_shares(x_shares[k-1]), 'y_inputs': serialize_shares(y_shares[k-1])}
			host, port = v
			tasks.append(talk_to_single_server(msg, host, port, self.certfile, self.keyfile, self.cafile))
		vals = []
		for res in asyncio.as_completed(tasks, timeout=CLIENT_TIMEOUT):
			msg = await res
			if msg != None:
				vals.append(deserialize_shares(msg['result']))
			if len(vals) > self.t:
				break
		if len(vals) < self.t+1:
			raise ValueError(f'Failed to receive enough server responses (got: {len(vals)}, need: {self.t+1})')
		return Shamir(self.t, self.n).reconstruct_bitstring_secret(vals)

async def talk_to_single_server(msg, host, port, cert, keyfile, cafile):
	ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
	ssl_ctx.options |= ssl.OP_NO_TLSv1
	ssl_ctx.options |= ssl.OP_NO_TLSv1_1
	ssl_ctx.load_cert_chain(cert, keyfile=keyfile)
	ssl_ctx.load_verify_locations(cafile=cafile)
	ssl_ctx.check_hostname = False
	ssl_ctx.verify_mode = ssl.VerifyMode.CERT_REQUIRED
	ssl_ctx.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
	reader, writer = await asyncio.open_connection(host, port, ssl=ssl_ctx)
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
