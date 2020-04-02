# NOTE: MUST run local_mpc_network.py in a separate process for this test to work
from client import Client
from multiprocessing import Process, Queue

def run_client_op(c, val, uuid, q):
	r = c.send_operation(val, uuid)
	q.put(r)

if __name__ == '__main__':
	# NOTE: MUST run local_mpc_network.py in a separate process for this test to work
	idx2node={1: ('0.0.0.0', 8000), 2: ('0.0.0.0', 8001), 3: ('0.0.0.0', 8002)}
	clients = [Client(1,3, idx2node) for _ in range(2)]
	q = Queue()
	procs = [Process(target=run_client_op, args=(clients[i], 300+i, 'abc', q)) for i in range(2)]
	for p in procs:
		p.start()
	for p in procs:
		p.join()
	while not q.empty():
		assert int(q.get()) == 1, "numbers were within 50"
	print("PASS INTERSECT TEST")
	procs = [Process(target=run_client_op, args=(clients[i], 5000+(i*100), 'abcd', q)) for i in range(2)]
	for p in procs:
		p.start()
	for p in procs:
		p.join()
	while not q.empty():
		assert int(q.get()) == 0, "numbers were not within 50"
	print("PASS NONINTERSECT TEST")
	q.close()
	q.join_thread()

