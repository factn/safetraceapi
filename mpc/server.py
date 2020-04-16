from serialize import *
from triples import TripleGeneration
from shamir import Shamir
from circuit import Circuit, RuntimeCircuit
import asyncio, json, os, ssl

class Server:

	def __init__(self, port, t, n, index, bootstrap=[], circuit_dir=None, certfile=None, keyfile=None, cafile=None):
		self.port = port
		self.t = t
		self.n = n
		self.index = index
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
		self.intersection_circuit = Circuit(os.path.join(self.circuit_dir, 'dist32.txt'), ['V' for _ in range(32)]+['S' if i != 31 else 'V' for i in range(32)]+['S' if i != 31 else 'V' for i in range(32)]+['V' for i in range(96)])
		self.bootstrap = bootstrap
		self.loop = asyncio.get_event_loop()
		self.active_ops = {}
		self.mpc_peers = {}
		self.mpc_listeners = []

	def start(self):
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
		coro = asyncio.start_server(self.handle_connection, '0.0.0.0', self.port, ssl=ssl_ctx, loop=self.loop)
		server = self.loop.run_until_complete(coro)
		for host, port, index in self.bootstrap:
			self.loop.create_task(self.mpc_handshake(host, port, index))
		print(f'Server starting on {server.sockets[0].getsockname()}')
		try:
			self.loop.run_forever()
		except:
			pass
		for task in self.mpc_listeners:
			task.cancel()
		server.close()
		self.loop.run_until_complete(server.wait_closed())
		self.loop.close()

	async def handle_connection(self, reader, writer):
		try:
			#print('receiving new connection')
			data = await reader.readline()
			data = data.strip()
			msg = json.loads(data.decode())
			if msg['msgtype'] == 'mpc-handshake':
				await self.handle_mpc_handshake(reader, writer, msg)
			elif msg['msgtype'] == 'get-intersection':
				await self.handle_intersection_client(reader, writer, msg)
			else:
				raise ValueError()
		except:
			writer.close()

	async def handle_intersection_client(self, reader, writer, msg):
		with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'test_triples/{self.index}-10k'), 'r') as f:
			data = f.read()
		data = json.loads(data)
		triples = deserialize_triples(data['data'])
		print(f'Executing intersection operation {msg["uuid"]}')
		resp = await self.execute_intersection_operation(msg, 40.63500, -73.96000, 0.08, triples)
		r = json.dumps(resp)
		writer.write(str.encode(r+'\n'))
		await writer.drain()
		writer.close()

	async def handle_mpc_handshake(self, reader, writer, msg):
		recv_index = msg['index']
		for host, port, index in self.bootstrap:
			if index == recv_index:
				h, _ = writer.get_extra_info('peername')
				if h==host and msg['port']==port: 
					r = json.dumps({'msgtype': 'mpc-handshake', 'index': self.index})
					writer.write(str.encode(r+'\n'))
					await writer.drain()
					self.mpc_peers[index] = (reader, writer)
					print(f"added mpc peer index {index} -- ({len(self.mpc_peers)} total mpc peers)")
					t = self.loop.create_task(self.mpc_listener(index))
					self.mpc_listeners.append(t)
					return
		raise ValueError('failed mpc handshake')

	async def mpc_handshake(self, host, port, index):
		try:
			ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
			ssl_ctx.options |= ssl.OP_NO_TLSv1
			ssl_ctx.options |= ssl.OP_NO_TLSv1_1
			ssl_ctx.load_cert_chain(self.certfile, keyfile=self.keyfile)
			ssl_ctx.load_verify_locations(cafile=self.cafile)
			ssl_ctx.check_hostname = False
			ssl_ctx.verify_mode = ssl.VerifyMode.CERT_REQUIRED
			ssl_ctx.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
			reader, writer = await asyncio.open_connection(host, port, ssl=ssl_ctx)
			r = json.dumps({'msgtype': 'mpc-handshake', 'index': self.index, 'port': self.port})
			writer.write(str.encode(r+'\n'))
			await writer.drain()
			data = await reader.readline()
			data = data.strip()
			msg = json.loads(data.decode())
			if msg['msgtype'] != 'mpc-handshake' or msg['index'] != index:
				raise ValueError('failed mpc handshake')
			self.mpc_peers[index] = (reader, writer)
			print(f"added mpc peer index {index} -- ({len(self.mpc_peers)} total mpc peers)")
			t = self.loop.create_task(self.mpc_listener(index))
			self.mpc_listeners.append(t)
		except:
			try:
				writer.close()
			except:
				pass

	async def mpc_listener(self, index):
		while True:
			try:
				reader, writer = self.mpc_peers[index]
				#await writer.drain()
				data = await reader.readline()
				data = data.strip()
				msg = json.loads(data.decode())
				for k, v in self.active_ops.items():
					if k == msg['uuid']:
						v.put_nowait(msg)
			except:
				try:
					writer.close()
					del self.mpc_peers[index]
					print(f"deleted mpc peer index {index} -- ({len(self.mpc_peers)} total mpc peers)")
				except:
					pass
				break

	async def send_mpc_msg(self, index, msg):
		try:
			reader, writer = self.mpc_peers[index]
			m = json.dumps(msg)
			writer.write(str.encode(m+'\n'))
			await writer.drain()
			return index, True
		except Exception as e:
			print(e)
			try:
				writer.close()
				await writer.wait_closed()
				del self.mpc_peers[index]
			except:
				pass
			return index, False

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
						#print(f'Circuit {opid} Index {self.index} layer {i+1}: FAILED TO SEND TO {idx}')
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
