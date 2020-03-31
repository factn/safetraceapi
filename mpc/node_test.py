from node import MPCNode, run_triples_protocol, run_circuit_protocol
from multiprocessing import Process, Queue
from shamir import Shamir
from triples import gen_triples
import os, shutil

def triples_consumer(q, t, n):
	vals = []
	while len(vals) < n:
		if not q.empty():
			vals.append(q.get())
	n_triples = len(vals[0])
	for i in [0, 1, n_triples-2, n_triples-1]:
		trips = [vals[j][i] for j in range(n)]
		a_shares = [t.a for t in trips]
		b_shares = [t.b for t in trips]
		c_shares = [t.c for t in trips]
		a = Shamir(t, n).reconstruct_secret(a_shares)
		b = Shamir(t, n).reconstruct_secret(b_shares)
		c = Shamir(t, n).reconstruct_secret(c_shares)
		assert a*b==c, "triples are not equal"
	print("PASS TRIPLES TEST")

def circuit_consumer(q, t, n, result):
    vals = []
    while len(vals) < n:
        if not q.empty():
            vals.append(q.get())
    reconstructed = Shamir(t, n).reconstruct_bitstring_secret(vals)[::-1]
    print()
    assert eval('0b'+reconstructed) == eval('0b'+result), "result incorrect"
    print("PASS CIRCUIT TEST")

def test_node_triples_protocol():
	nodes = []
	t = 1
	n = 3
	idx2peer = {1: ('0.0.0.0', 8000), 2: ('0.0.0.0', 8001), 3: ('0.0.0.0', 8002)}
	homedir = os.path.expanduser("~")
	mpc_dir = os.path.join(homedir, ".mpc_msg")
	try:
		os.mkdir(mpc_dir)
	except:
		pass
	for i in range(1,n+1):
		d = {}
		for k, v in idx2peer.items():
			if k != i:
				d[k] = v
			else:
				d[k] = None
		os.mkdir(os.path.join(mpc_dir, f"{i}"))
		node = MPCNode(t, n, i, 7999+i, os.path.join(mpc_dir, f"{i}"), d)
		nodes.append(node)
	for node in nodes:                                                   
		node.start()
	q = Queue()
	procs = []
	for node in nodes:
		p = Process(target=run_triples_protocol, args=(node, 'abc', q, 10, 5))
		procs.append(p)
	for p in procs:
		p.start()
	c = Process(target=triples_consumer, args=(q, t, n))
	c.start()
	c.join()
	while not q.empty():
		q.get()
	q.close()
	for p in procs:
		p.terminate()
	shutil.rmtree(mpc_dir)
	q.join_thread()
	for node in nodes:
		node.stop()

def test_node_circuit_protocol():
	nodes = []
	t = 1
	n = 3
	idx2peer = {1: ('0.0.0.0', 8000), 2: ('0.0.0.0', 8001), 3: ('0.0.0.0', 8002)}
	homedir = os.path.expanduser("~")
	mpc_dir = os.path.join(homedir, ".mpc_msg")
	try:
		os.mkdir(mpc_dir)
	except:
		pass
	for i in range(1,n+1):
		d = {}
		for k, v in idx2peer.items():
			if k != i:
				d[k] = v
			else:
				d[k] = None
		os.mkdir(os.path.join(mpc_dir, f"{i}"))
		node = MPCNode(t, n, i, 7999+i, os.path.join(mpc_dir, f"{i}"), d)
		nodes.append(node)
	for node in nodes:                                                   
		node.start()
	x = 35
	y = 500
	result = bin(x+y)[2:]
	triples = gen_triples(t, n, 500)
	x_bin = bin(x)[2:]
	while len(x_bin) < 64:
		x_bin = '0'+x_bin
	y_bin = bin(y)[2:]
	while len(y_bin) < 64:
		y_bin = '0'+y_bin
	x_bin = x_bin[::-1]
	y_bin = y_bin[::-1]
	shares = Shamir(t, n).share_bitstring_secret(x_bin+y_bin)
	q = Queue()
	procs = []
	for i in range(len(nodes)):
		p = Process(target=run_circuit_protocol, args=(nodes[i], 'abc', q, 'bristol_circuits/add64.txt', shares[i], triples[i]))
		procs.append(p)
	for p in procs:
		p.start()
	c = Process(target=circuit_consumer, args=(q, t, n, result))
	c.start()
	c.join()
	while not q.empty():
		q.get()
	q.close()
	for p in procs:
		p.terminate()
	shutil.rmtree(mpc_dir)
	q.join_thread()
	for node in nodes:
		node.stop()

if __name__ == "__main__":
	test_node_triples_protocol()
	test_node_circuit_protocol()