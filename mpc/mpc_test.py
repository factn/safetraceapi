from circuit import Circuit
from shamir import Shamir, Share, gen_triples
from messenger import MockMessenger
from multiprocessing import Queue, Process

def run_circuit_process(t, n, c_path, index, queues, main_queue, inputs, triples):
	print(f"starting node {index}")
	shamir = Shamir(t, n)
	messenger = MockMessenger(t, n, index, queues)
	c = Circuit(c_path)
	outputs = c.evaluate(inputs, shamir=shamir, messenger=messenger, triples=triples)
	main_queue.put(outputs)
	print(f"closing node {index}")

def test_mul32_circuit():
	t = 2
	n = 5
	c_path = "circuits/mul32_circuit.txt"
	triples = gen_triples(t, n, 8000)
	mq = Queue()
	queues = [Queue() for _ in range(n)]
	x = 101
	y = 50000
	result = x*y
	x_bin = bin(x)[2:]
	while len(x_bin)<32:
		x_bin = '0'+x_bin
	y_bin = bin(y)[2:]
	while len(y_bin)<32:
		y_bin = '0'+y_bin
	x_shares = Shamir(t, n).share_bitstring_secret(x_bin)
	y_shares = Shamir(t, n).share_bitstring_secret(y_bin)
	processes = []
	for i in range(n):
		p = Process(target=run_circuit_process, args=(t, n, c_path, i+1, queues, mq, x_shares[i]+y_shares[i], triples[i]))
		processes.append(p)
	for p in processes:
		p.start()
	vals = []
	while len(vals)<n:
		if not mq.empty():
			vals.append(mq.get())
	reconstructed = Shamir(t, n).reconstruct_bitstring_secret(vals)
	print("result:", reconstructed)
	assert eval('0b'+reconstructed) == result, "result incorrect"
	print("TEST PASSED")
	# TO DO: These processes aren't properly closing, so the test stalls here...
	# Probably something to do with some processes being locked/stalled? 
	for p in processes:
		p.join()
	for q in queues:
		q.close()
		q.join_thread()
	mq.close()
	mq.join_thread()

def test_tiny_circuit():
	t = 2
	n = 5
	c_path = "circuits/tiny_circuit.txt"
	triples = gen_triples(t, n, 2)
	mq = Queue()
	queues = [Queue() for _ in range(n)]
	x = '01'
	y = '10'
	result = '11'
	x_shares = Shamir(t, n).share_bitstring_secret(x)
	y_shares = Shamir(t, n).share_bitstring_secret(y)
	processes = []
	for i in range(n):
		p = Process(target=run_circuit_process, args=(t, n, c_path, i+1, queues, mq, x_shares[i]+y_shares[i], triples[i]))
		processes.append(p)
	for p in processes:
		p.start()
	vals = []
	while len(vals)<n:
		if not mq.empty():
			vals.append(mq.get())
	reconstructed = Shamir(t, n).reconstruct_bitstring_secret(vals)
	print("result:", reconstructed)
	assert reconstructed == result, "result incorrect"
	print("TEST PASSED")
	for p in processes:
		p.join()
	for q in queues:
		q.close()
		q.join_thread()
	mq.close()
	mq.join_thread()

if __name__ == "__main__":
	print("--BEGIN SHORT TEST (4 gates)--")
	test_tiny_circuit()
	print("--BEGIN LONG TEST (12374 gates)--")
	test_mul32_circuit()
