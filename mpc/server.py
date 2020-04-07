import p2p
from serialize import *
from triples import TripleGeneration
from shamir import Shamir
from dispatcher import Dispatcher
from circuit import Circuit
from multiprocessing import Process, Queue
import asyncio, json, os

class Server:

	def __init__(self, node_port, t, n, index, idx2peer, circuit_dir=None):
		self.port = node_port
		self.t = t
		self.n = n
		self.index = index
		self.idx2peer = idx2peer
		self.queues = [Queue() for _ in range(self.n)]
		self.circuit_dir = circuit_dir
		if self.circuit_dir == None:
			self.circuit_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bristol_circuits')
		self.mpc_server = None
		mpc_send_queues = {}
		for i in range(1, self.n+1):
			host, port = self.idx2peer[i]
			if i==self.index:
				mpc_recv_queue = self.queues[self.index-1]
				self.mpc_server = Process(target=p2p.run_mpc_msg_receiver, args=(port, mpc_recv_queue))
			else:
				mpc_send_queues[self.idx2peer[i]] = self.queues[i-1]
		self.mpc_client = Process(target=p2p.run_mpc_msg_sender, args=(mpc_send_queues,))
		self.active_operations = {}

	def start_mpc_server(self):
		if not self.mpc_server.is_alive():
			self.mpc_server.start()

	def stop_mpc_server(self):
		if self.mpc_server.is_alive():
			self.mpc_server.terminate()
		try:
			q = self.queues[self.index-1]
			while not q.empty():
				q.get()
			q.close()
			q.join_thread()
		except:
			pass

	def start_mpc_client(self):
		if not self.mpc_client.is_alive():
			self.mpc_client.start()

	def stop_mpc_client(self):
		if self.mpc_client.is_alive():
			self.mpc_client.terminate()
		for i in range(len(self.queues)):
			if i+1 != self.index:
				try:
					while not self.queues[i].empty():
						self.queues[i].get()
					self.queues[i].close()
					self.queues[i].join_thread()
				except:
					pass

	def start(self):
		loop = asyncio.get_event_loop()
		coro = asyncio.start_server(self.handle_client, '0.0.0.0', self.port, loop=loop)
		server = loop.run_until_complete(coro)
		print(f'Server starting on {server.sockets[0].getsockname()}')
		try:
			loop.run_forever()
		except KeyboardInterrupt:
			pass
		server.close()
		loop.run_until_complete(server.wait_closed())
		loop.close()

	async def handle_client(self, reader, writer):
		try:
			data = await reader.readline()
			data = data.strip()
			msg = json.loads(data.decode())
			if msg['uuid'] in self.active_operations:
				print(f"Execute operation {msg['uuid']}")
				resp = await self.execute_operation(msg)
				r = json.dumps(resp)
				writer.write(str.encode(r+'\n'))
				await writer.drain()
				self.active_operations[msg['uuid']][2].write(str.encode(r+'\n'))
				await self.active_operations[msg['uuid']][2].drain()
				self.active_operations[msg['uuid']][2].close()
				self.active_operations.pop(msg['uuid'], None)
				writer.close()
			else:
				print(f"Queue operation {msg['uuid']}")
				inputs = deserialize_shares(msg['inputs'])
				# TODO: TRIPLES CURRENTLY MOCKED (should be distributedly created in the background, and never reused) THIS BREAKS SECURITY.
				with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'test_triples/{self.index}'), 'r') as f:
					data = f.read()
				data = json.loads(data)
				triples = deserialize_triples(data['data'])
				self.active_operations[msg['uuid']] = (inputs, triples, writer)
		except:
			writer.close()

	async def execute_operation(self, msg):
		inputs2 = deserialize_shares(msg['inputs'])
		inputs1 = self.active_operations[msg['uuid']][0]
		triples = self.active_operations[msg['uuid']][1]
		m = Dispatcher(self.t, self.n, self.index, self.queues, msg['uuid']+'-sub')
		s = Shamir(self.t, self.n)
		subtract = Circuit(os.path.join(self.circuit_dir, 'sub64.txt'), ['S' for _ in range(128)])
		outputs1 = subtract.evaluate(inputs1+inputs2, shamir=s, dispatcher=m, triples=triples[:300])
		triples = triples[300:]
		m.uuid = msg['uuid']+'-mul'
		mul = Circuit(os.path.join(self.circuit_dir, 'mul64mod.txt'), ['S' for _ in range(128)])
		outputs2 = mul.evaluate(outputs1+outputs1, shamir=s, dispatcher=m, triples=triples[:5000])
		triples = triples[5000:]
		m.uuid = msg['uuid']+'-eqz'
		eqz = Circuit(os.path.join(self.circuit_dir, 'eqzero64.txt'), ['S' for _ in range(32)]+['V' for _ in range(32)])
		bit1 = eqz.evaluate(outputs2[32:]+[0 for _ in range(32)], shamir=s, dispatcher=m, triples=triples[200:])
		triples = triples[200:]
		m.uuid = msg['uuid']+'-lt'
		br = bin(1000000)[2:] # Hardcoded radius of intersection r = 1000
		while len(br) < 32:
			br = '0'+br
		lt = Circuit(os.path.join(self.circuit_dir, 'lessthan32.txt'), ['S' for _ in range(32)]+['V' for _ in range(32)])
		bit2 = lt.evaluate(outputs2[:32]+[int(i) for i in br[::-1]], shamir=s, dispatcher=m, triples=triples[400:])
		triples = triples[:400]
		m.uuid = msg['uuid']+'-and'
		bit1.extend(bit2)
		c = Circuit(os.path.join(self.circuit_dir, 'mul2.txt'), ['S' for _ in range(2)])
		out = c.evaluate(bit1, shamir=s, dispatcher=m, triples=triples)
		return {'uuid': msg['uuid'], 'result': serialize_shares(out)}	
