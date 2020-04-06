import socket, select, json

def recv_mpc_msgs(port, queue):
	connections = []
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.setblocking(0)
	server_socket.bind(('0.0.0.0', port))
	server_socket.listen(10)

	# Add server socket to the list of readable connections
	connections.append(server_socket)

	print('mpc server started on port ' + str(port))

	while True:
		# Get the list sockets which are ready to be read through select
		read_sockets, _, _ = select.select(connections,[],[])

		for sock in read_sockets:
			
			#New connection
			if sock == server_socket:
				sockfd, addr = server_socket.accept()
				sockfd.setblocking(0)
				connections.append(sockfd)
				#print(f'mpc client {addr[0]}:{addr[1]} connected')		
			#Some incoming message from a client
			else:
				try:
					data = sock.recv(1024)
					while data.decode()[-1] != '\n':
						data += sock.recv(1024)
					data = data.strip()
					msg = json.loads(data.decode())
					#print(f"receiving on socket: {msg}")
					queue.put(msg)
				
				# client disconnected, so remove from socket list
				except Exception as e:
					#print(f'mpc client disconnected because: {e}')
					sock.close()
					connections.remove(sock)
					continue
		
	server_socket.close()

def send_mpc_msgs(peer2q):
	sockets = []
	queues = []
	for k, v in peer2q.items():
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((k[0], k[1]))
		sockets.append(s)
		queues.append(v)
	while True:
		for i in range(len(queues)):
			if not queues[i].empty():
				msg = queues[i].get()
				v = json.dumps(msg)
				try:
					sockets[i].sendall(str.encode(v+'\n'))
				except:
					try:
						sockets[i].close()
					except:
						#print("failed to close")
						pass
					queues[i].put(msg)
					try:
						sockets[i].connect()
					except:
						#print("failed to reconnect")
						pass
	for s in sockets:
		s.close()


