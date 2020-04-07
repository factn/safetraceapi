import json, asyncio

async def recv_mpc_msgs(reader, writer, queue):
	while True:
		try:
			data = await reader.readline()
			data = data.strip()
			msg = json.loads(data.decode())
			queue.put(msg)
		except:
			writer.close()
			break

def run_mpc_msg_receiver(port, queue):
	loop = asyncio.get_event_loop()
	coro = asyncio.start_server(lambda r, w: recv_mpc_msgs(r, w, queue), '0.0.0.0', port, loop=loop)
	server = loop.run_until_complete(coro)
	print(f'MPC msg receiver starting on {server.sockets[0].getsockname()}')
	try:
		loop.run_forever()
	except KeyboardInterrupt:
		pass
	server.close()
	loop.run_until_complete(server.wait_closed())
	loop.close()

async def send_mpc_msg(writers, queues, peers, i):
	msg = queues[i].get()
	v = json.dumps(msg)
	try:
		writers[i].write(str.encode(v+'\n'))
		await writers[i].drain()
	except:
		queues[i].put(msg)
		writers[i].close()
		await writers[i].wait_closed()
		_, new_writer = await asyncio.open_connection(peers[i][0], peers[i][1])
		writers[i] = new_writer

async def send_mpc_msgs(peer2q):
	peers = []
	queues = []
	writers = []
	for k, v in peer2q.items():
		_, writer = await asyncio.open_connection(k[0], k[1])
		writers.append(writer)
		queues.append(v)
		peers.append(k)
	while True:
		sends = [send_mpc_msg(writers, queues, peers, i) for i in range(len(queues)) if not queues[i].empty()]
		await asyncio.gather(*sends)

def run_mpc_msg_sender(peer2q):
	asyncio.run(send_mpc_msgs(peer2q))
