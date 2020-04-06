# NOTE: MUST run local_mpc_network.py in a separate process for this test to work
from client import Client
from multiprocessing import Process, Queue
import random, time

def run_client_op(c, val, uuid, q):
	r = c.send_operation(val, uuid)
	q.put(r)

def test_mpc_intersection(clients):
	q = Queue()
	pid1 = ''.join([random.choice([i for i in 'abcdef123456789']) for _ in range(10)])
	nums = [random.choice(range(1,3001)) for _ in range(2)]
	result = 0
	if (nums[0]-nums[1])**2 < 1000**2:
		result = 1
	procs = [Process(target=run_client_op, args=(clients[i], nums[i], pid1, q)) for i in range(2)]
	start = time.time()
	for p in procs:
		p.start()
	for p in procs:
		p.join()
	print(f'operation time: {round(time.time()-start, 4)}')
	while not q.empty():
		assert int(q.get()) == result, "reconstructed wrong result"
	print("PASS INTERSECTION TEST")
	q.close()
	q.join_thread()

if __name__ == '__main__':
	# NOTE: MUST run local_mpc_network.py in a separate process for this test to work
	idx2node={1: ('0.0.0.0', 8000), 2: ('0.0.0.0', 8001), 3: ('0.0.0.0', 8002)}
	clients = [Client(1,3, idx2node) for _ in range(2)]
	for i in range(3):
		test_mpc_intersection(clients)


