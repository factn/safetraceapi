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
		self.active_operations = []
		self.circuit = Circuit(os.path.join(self.circuit_dir, 'dist32.txt'), ['V' for _ in range(32)]+['S' if i != 31 else 'V' for i in range(32)]+['S' if i != 31 else 'V' for i in range(32)]+['V' for i in range(96)])

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
			print(f'Executing operation {msg["uuid"]}')
			with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'test_triples/{self.index}'), 'r') as f:
				data = f.read()
			data = json.loads(data)
			triples = deserialize_triples(data['data'])
			resp = await self.execute_operation(msg, 40.63500, -73.96000, 0.08, triples)
			r = json.dumps(resp)
			writer.write(str.encode(r+'\n'))
			await writer.drain()
			writer.close()
		except:
			writer.close()

	async def execute_operation(self, msg, c_x, c_y, r, triples):
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
		d = Dispatcher(self.t, self.n, self.index, self.queues, msg['uuid'])
		s = Shamir(self.t, self.n)
		out = await self.circuit.evaluate(inputs, shamir=s, dispatcher=d, triples=triples)
		return {'uuid': msg['uuid'], 'result': serialize_shares(out)}
