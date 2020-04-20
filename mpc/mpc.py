from serialize import *
from shamir import Shamir
from circuit import Circuit, RuntimeCircuit
from hashlib import sha256
from ecies import encrypt, decrypt, hex2prv
import asyncio, aiohttp, ssl
import json, base64, binascii, random, time, os

class MPCProtocol(asyncio.Protocol):

	def __init__(self, local_peer, client=False):
		self.mpc = local_peer
		self.peer_index = None
		self.current_line = ''
		self.transport = None
		self.client = client

	def connection_made(self, transport):
		self.transport = transport
		peername = self.transport.get_extra_info('peername')
		print(f'Peer {self.mpc.index} received new connection from {peername}')
		if self.client:
			msg = json.dumps({'msgtype': 'bootstrap', 'index': self.mpc.index, 'port':self.mpc.port, 'ptype': self.mpc.protocol_type}) + '\n'
			self.transport.write(msg.encode())

	def data_received(self, data):
		self.current_line += data.decode()
		if len(self.current_line) == 0 or self.current_line[-1] != '\n':
			return
		else:
			try:
				msg = json.loads(self.current_line)
				if msg['msgtype'] == 'bootstrap':
					self.handle_bootstrap_msg(msg)
				elif msg['msgtype'] == 'mpc':
					self.handle_mpc_msg(msg)
				elif msg['msgtype'] == 'triple-id':
					self.handle_triple_id_msg(msg)
			except:
				pass
			self.current_line = ''

	def connection_lost(self, exception):
		if self.peer_index != None:
			del self.mpc.peers[self.peer_index]
			print(f"Peer {self.mpc.index} disconnected from peer {self.peer_index} -- ({len(self.mpc.peers)} total peers)")

	def handle_mpc_msg(self, msg):
		op_round = self.mpc.active_ops[msg['pid']][msg['round']]
		if self.peer_index not in op_round.keys():
			if msg['datatype'] == "TRIP-AB":
				data = deserialize_triple_ab_msg(msg['data'])
			elif msg['datatype'] == "TRIP-C":
				data = deserialize_triple_c_msg(msg['data'])
			elif msg['datatype'] == "MUL":
				data = deserialize_mul_msg(msg['data'])
			else:
				raise ValueError(f"Unrecognized mpc msgtype: {msg['msgtype']}")
			op_round[self.peer_index] = data

	def send_mpc_msg(self, data, data_type, pid, round_n):
		msg = json.dumps({'msgtype': 'mpc', 'data': data, 'datatype':data_type, 'pid': pid, 'round': round_n}) + '\n'
		self.transport.write(msg.encode())

	def handle_bootstrap_msg(self, msg):
		peername = self.transport.get_extra_info('peername')
		try:
			found = False
			for host, port, index in self.mpc.bootstrap:
				if (host == peername[0]) and (msg['port'] == port) and (msg['index'] == index) and (msg['ptype'] == self.mpc.protocol_type):
					self.mpc.peers[index] = self
					self.peer_index = index
					print(f"Peer {self.mpc.index} added peer {self.peer_index} -- ({len(self.mpc.peers)} total peers)")
					found = True
			if not found:
				raise ValueError("not in bootstrap list")
		except Exception as e:
			print(f"Disconnecting from {peername}: {e}")
			self.transport.close()
		if not self.client:
			resp = json.dumps({'msgtype': 'bootstrap', 'index': self.mpc.index, 'port':self.mpc.port, 'ptype': self.mpc.protocol_type}) + '\n'
			self.transport.write(resp.encode())
		if len(self.mpc.peers) == self.mpc.n-1:
			if self.mpc.protocol_type == 'TRIPLE':
				try:
					self.mpc.triple_task.cancel()
				except:
					pass
				self.mpc.triple_task = self.mpc.loop.create_task(self.mpc.triples_loop())
			if self.mpc.protocol_type == 'MPC':
				self.mpc.loop.create_task(self.mpc.main_loop())

	def handle_triple_id_msg(self, msg):
		if self.peer_index not in self.mpc.triple_id.keys():
			self.mpc.triple_id[self.peer_index] = msg['id']

	def send_triple_id_msg(self, id_):
		msg = json.dumps({'msgtype': 'triple-id', 'id': id_}) + '\n'
		self.transport.write(msg.encode())

class MPCPeer:

	def __init__(self, port, t, n, index, priv_hex, bootstrap, protocol_type, circuit_dir=None, certfile=None, keyfile=None, cafile=None, api_endpoint=None, api_key=None):
		self.port = port
		self.t = t
		self.n = n
		self.index = index
		self.private_key = priv_hex
		self.bootstrap = bootstrap
		self.protocol_type = protocol_type
		self.circuit_dir = circuit_dir
		if self.circuit_dir == None:
			self.circuit_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bristol_circuits')
		self.certfile = certfile
		if self.certfile == None:
			self.certfile = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certs'), f'node-{self.index}-test.crt')
		self.keyfile = keyfile
		if self.keyfile == None:
			self.keyfile = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certs'), f'node-{self.index}-test.key')
		self.cafile = cafile
		if self.cafile == None:
			self.cafile = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certs'), 'testCA.pem')
		self.api_endpoint = api_endpoint
		self.api_key = api_key
		self.loop = asyncio.get_event_loop()
		self.shamir = Shamir(self.t, self.n)
		self.public_key = binascii.hexlify(hex2prv(self.private_key).public_key.format(True)).decode()
		self.peers = {}
		self.active_ops = {}
		self.triples = []
		self.triple_id = {}
		self.triple_task = None

	def start(self):
		self.loop.run_until_complete(self.bootstrap_and_start())
		try:
			self.loop.run_forever()
		except KeyboardInterrupt:
			pass
		self.loop.close()

	async def bootstrap_and_start(self):
		ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
		ssl_ctx.options |= ssl.OP_NO_TLSv1
		ssl_ctx.options |= ssl.OP_NO_TLSv1_1
		ssl_ctx.options |= ssl.OP_SINGLE_DH_USE
		ssl_ctx.options |= ssl.OP_SINGLE_ECDH_USE
		ssl_ctx.load_cert_chain(self.certfile, self.keyfile)
		ssl_ctx.load_verify_locations(cafile=self.cafile)
		ssl_ctx.check_hostname = False
		ssl_ctx.verify_mode = ssl.VerifyMode.CERT_REQUIRED
		ssl_ctx.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
		server = await self.loop.create_server(lambda: MPCProtocol(self), '127.0.0.1', self.port, ssl=ssl_ctx, start_serving=False)
		print(f'Peer {self.index} starting at 127.0.0.1:{self.port}')
		for host, port, index in self.bootstrap:
			try:
				await self.connect_to_mpc_peer(host, port, index)
			except:
				pass
		async with server:
			await server.serve_forever()

	async def main_loop(self):
		pass
		# TODO

	async def triples_loop(self):
		global_start = time.time()
		print('starting triples loop')
		self.triples = []
		self.active_ops['TRIPLES'] = {}
		while len(self.peers) == self.n-1:
			self.active_ops['TRIPLES'] = {i+1: {} for i in range(2)}
			self.triple_id = {}
			start = time.time()
			triples = await asyncio.wait_for(self.generate_triples(10000), timeout=30)
			self.triples.extend(triples)
			print(f"triples: {len(self.triples)}, time: {round(time.time()-start, 4)}")
			if len(self.triples) == 1000000:
				my_id = ''.join([random.choice('abcdef0123456789') for _ in range(10)])
				self.triple_id[self.index] = my_id
				for i in range(1, self.n+1):
					if i != self.index:
						self.peers[i].send_triple_id_msg(my_id)
				id_ = await self.gather_triple_id()
				print(f"triples id: {id_} time: {round(time.time()-global_start, 4)}")
				data = serialize_triples(self.triples)
				self.triples = []
				shrs = json.dumps({'data': data})
				encrypted_shares = encrypt(self.public_key, shrs.encode())
				msg = {'share': base64.b64encode(encrypted_shares).decode(), 'triple_id': id_[:10], 'node_id': self.index, 'api_key': self.api_key}
				print("share length:", len(msg['share']))
				if self.api_endpoint != None:
					r = await post_request(self.api_endpoint, msg)
					print("triples posted:", r)
				else:
					print("no api address set - not posting")
				global_start = time.time()
		print('ending triples loop')

	async def connect_to_mpc_peer(self, host, port, index):
		ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
		ssl_ctx.options |= ssl.OP_NO_TLSv1
		ssl_ctx.options |= ssl.OP_NO_TLSv1_1
		ssl_ctx.load_cert_chain(self.certfile, keyfile=self.keyfile)
		ssl_ctx.load_verify_locations(cafile=self.cafile)
		ssl_ctx.check_hostname = False
		ssl_ctx.verify_mode = ssl.VerifyMode.CERT_REQUIRED
		ssl_ctx.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
		await asyncio.wait_for(self.loop.create_connection(lambda: MPCProtocol(self, client=True), host, port, ssl=ssl_ctx), timeout=5)

	async def generate_triples(self, batch_size):
		msgs = self.shamir.generate_triples_round_1(batch_size)
		for i in range(1, self.n+1):
			if i != self.index:
				self.peers[i].send_mpc_msg(serialize_triple_ab_msg(msgs[i-1]), "TRIP-AB", "TRIPLES", 1)
		resps = await self.gather_mpc_msgs("TRIPLES", 1, self.n-1)
		resps.append(msgs[self.index-1])
		a_shares, b_shares, msgs = self.shamir.generate_triples_round_2(resps)
		for i in range(1, self.n+1):
			if i != self.index:
				self.peers[i].send_mpc_msg(serialize_triple_c_msg(msgs[i-1]), "TRIP-C", "TRIPLES", 2)
		resps = await self.gather_mpc_msgs("TRIPLES", 2, self.n-1)		
		resps.append(msgs[self.index-1])
		return self.shamir.generate_triples_round_3(a_shares, b_shares, resps)

	async def gather_mpc_msgs(self, pid, round_n, target_n):
		while len(self.active_ops[pid][round_n]) < target_n:
			await asyncio.sleep(0.25)
		return [i for i in self.active_ops[pid][round_n].values()]

	async def gather_triple_id(self):
		while len(self.triple_id) < self.n:
			await asyncio.sleep(0.25)
		raw_string = ''
		for i in range(1, self.n+1):
			for k, v in self.triple_id.items():
				if k == i:
					raw_string += v
					break
		return sha256(raw_string.encode()).hexdigest()


async def post_request(url, data):
	async with aiohttp.ClientSession() as session:
		async with session.post(url, json=data) as resp:
			return await resp.text()

async def get_request(url, data):
	async with aiohttp.ClientSession() as session:
		async with session.get(url, params=data) as resp:
			return await resp.text()

'''
	--KEEPING FOR REFERENCE--
	async def execute_intersection_operation(self, msg, c_x, c_y, r, triples):
		x_inputs = deserialize_shares(msg['x_inputs'])
		y_inputs = deserialize_shares(msg['y_inputs'])
		if len(x_inputs) != 31 or len(y_inputs) != 31:
			return {'status': 'fail', 'reason':'inputs must be exactly 31 bits'}
		x_inputs.append(0)
		y_inputs.append(0)
		rsq = round((r*100000))**2
		c_x = round((c_x + 90)*100000)
		c_y = round((c_y + 180)*100000)
		cx_bits = [int(b) for b in bin(c_x)[2:]]
		cy_bits = [int(b) for b in bin(c_y)[2:]]
		rsq_bits = [int(b) for b in bin(rsq)[2:]]
		all_constant_bits = []
		for bits in (cx_bits, cy_bits, rsq_bits):
			if len(bits) < 32:
				cbs = [0 for _ in range(32-len(bits))]+ bits
				all_constant_bits.extend(cbs[::-1])
		inputs = [0 for _ in range(32)]+x_inputs+y_inputs+all_constant_bits
		opid = msg['uuid']
		self.active_ops[opid] = asyncio.Queue()
		runtime = RuntimeCircuit(self.intersection_circuit, inputs, triples=triples, shamir=Shamir(self.t, self.n))
		for i in range(len(runtime.circuit_layers)):
			idxs, x, y, send_shares, cs = runtime.compute_layer(i)
			bmsg = serialize_mul_msg(send_shares)
			m = {'uuid': opid, 'round': i, 'data': bmsg}
			tasks = []
			for k in range(1, self.n+1):
				if k != self.index:
					tasks.append(self.send_mpc_msg(k, m))
			while len(tasks) > 0:
				new_tasks = []
				for res in asyncio.as_completed(tasks):
					idx, ok = await res
					if not ok:
						print(f'Circuit {opid} Index {self.index} layer {i+1}: FAILED TO SEND TO {idx}')
						for host, port, nidx in self.bootstrap:
							if nidx == idx:
								self.loop.create_task(self.mpc_handshake(host, port, nidx))
						new_tasks.append(self.send_mpc_msg(idx, m))
				tasks = new_tasks
			resps = []
			while len(resps) < self.t+1:
				r = await self.active_ops[opid].get()
				if r['round'] == i:
					resps.append(deserialize_mul_msg(r['data']))
				elif r['round'] > i:
					self.active_ops[opid].put_nowait(r)
			resps.append(send_shares)
			runtime.finish_layer(idxs, x, y, resps, cs)
		out = runtime.get_outputs()
		del self.active_ops[opid]
		return {'uuid': opid, 'result': serialize_shares(out)}
'''
