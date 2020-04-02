from p2p import receive_to_queue, send_from_queue
from serialize import *
from triples import TripleGeneration
from shamir import Shamir
from messenger import Messenger
from circuit import Circuit
from multiprocessing import Process, Queue
import socket, select, json, os

class Node:

	def __init__(self, node_port, t, n, index, idx2peer, circuit_dir=None):
		self.port = node_port
		self.t = t
		self.n = n
		self.index = index
		self.idx2peer = idx2peer
		self.queues = [Queue() for _ in range(self.n)]
		self.mpc_clients = []
		self.circuit_dir = circuit_dir
		if self.circuit_dir == None:
			self.circuit_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bristol_circuits')
		self.mpc_server = None
		for i in range(1, self.n+1):
			host, port = self.idx2peer[i]
			if i==self.index:
				self.mpc_server = Process(target=receive_to_queue, args=(port, self.queues[i-1]))
			else:
				self.mpc_clients.append(Process(target=send_from_queue, args=(host, port, self.queues[i-1])))

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


	def start_mpc_clients(self):
		for c in self.mpc_clients:
			c.start()

	def stop_mpc_clients(self):
		for c in self.mpc_clients:
			if c.is_alive():
				c.terminate()
		for i in range(len(self.queues)):
			if i != self.index-1:
				try:
					q = self.queues[i]
					while not q.empty():
						q.get()
					q.close()
					q.join_thread()
				except:
					pass		

	def start(self):
		connections = []
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind(('0.0.0.0', self.port))
		server_socket.listen(10)

		# Add server socket to the list of readable connections
		connections.append(server_socket)

		print(f'node {self.index} started on port ' + str(self.port))
		queued_intersections = {}

		while True:
			# Get the list sockets which are ready to be read through select
			read_sockets, _, _ = select.select(connections,[],[])

			for sock in read_sockets:
				
				#New connection
				if sock == server_socket:
					sockfd, addr = server_socket.accept()
					connections.append(sockfd)
					print(f'Client {addr[0]}:{addr[1]} connected')		
				#Some incoming message from a client
				else:
					try:
						data = sock.recv(1024)
						while data.decode()[-1] != '\n':
							data += sock.recv(1024)
						data = data.strip()
						msg = json.loads(data.decode())
						if msg['uuid'] == "KILL":
							server_socket.close()
							return
						if msg['uuid'] in queued_intersections:
							inputs2 = deserialize_shares(msg['inputs'])
							inputs1 = queued_intersections[msg['uuid']][0]
							triples = queued_intersections[msg['uuid']][1]
							m = Messenger(self.t, self.n, self.index, self.queues, msg['uuid']+'-sub')
							s = Shamir(self.t, self.n)
							subtract = Circuit(os.path.join(self.circuit_dir, 'sub64.txt'), ['S' for _ in range(128)])
							outputs1 = subtract.evaluate(inputs1+inputs2, shamir=s, messenger=m, triples=triples[:300])
							triples = triples[300:]
							m.uuid = msg['uuid']+'-mul'
							mul = Circuit(os.path.join(self.circuit_dir, 'mul64mod.txt'), ['S' for _ in range(128)])
							outputs2 = mul.evaluate(outputs1+outputs1, shamir=s, messenger=m, triples=triples[:5000])
							triples = triples[5000:]
							m.uuid = msg['uuid']+'-z'
							eqz = Circuit(os.path.join(self.circuit_dir, 'eqzero64.txt'), ['S' for _ in range(32)]+['V' for _ in range(32)])
							bit1 = eqz.evaluate(outputs2[32:]+[0 for _ in range(32)], shamir=s, messenger=m, triples=triples[200:])
							triples = triples[200:]
							m.uuid = msg['uuid']+'-lt'
							br = bin(2500)[2:]
							while len(br) < 32:
								br = '0'+br
							lt = Circuit(os.path.join(self.circuit_dir, 'lessthan32.txt'), ['S' for _ in range(32)]+['V' for _ in range(32)])
							bit2 = lt.evaluate(outputs2[:32]+[int(i) for i in br[::-1]], shamir=s, messenger=m, triples=triples[400:])
							triples = triples[:400]
							m.uuid = msg['uuid']
							bit1.extend(bit2)
							c = Circuit(os.path.join(self.circuit_dir, 'mul2.txt'), ['S' for _ in range(2)])
							out = c.evaluate(bit1, shamir=s, messenger=m, triples=triples)
							res_msg = {'uuid': msg['uuid'], 'result': serialize_shares(out)}
							res = json.dumps(res_msg)
							sock.sendall(str.encode(res+'\n'))
							queued_intersections[msg['uuid']][2].sendall(str.encode(res+'\n'))
							del queued_intersections[msg['uuid']]
						else:
							inputs = deserialize_shares(msg['inputs'])
							m = Messenger(self.t, self.n, self.index, self.queues, msg['uuid']+'-triples')
							tg = TripleGeneration(self.index, Shamir(self.t, self.n), m, batch_size=1000, n_batches=6)
							tg.run()
							queued_intersections[msg['uuid']] = (inputs, tg.triples, sock)
							# client disconnected, so remove from socket list
					except:
						print(f'Client disconnected')
						sock.close()
						connections.remove(sock)
						continue
			
		server_socket.close()
