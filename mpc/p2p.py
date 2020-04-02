import socket, select, json

def receive_to_queue(port, queue):
	connections = []
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
				connections.append(sockfd)
				print(f'mpc client {addr[0]}:{addr[1]} connected')		
			#Some incoming message from a client
			else:
				try:
					data = sock.recv(1024)
					while data.decode()[-1] != '\n':
						data += sock.recv(1024)
					data = data.strip()
					msg = json.loads(data.decode())
					queue.put(msg)
				
				# client disconnected, so remove from socket list
				except:
					#print(f'mpc client disconnected')
					#sock.close()
					#connections.remove(sock)
					continue
		
	server_socket.close()

def send_from_queue(host, port, queue):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	while True:
		if not queue.empty():
			msg = queue.get()
			v = json.dumps(msg)
			s.sendall(str.encode(v+'\n'))
	s.close()
