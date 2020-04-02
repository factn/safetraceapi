from node import Node
from client import Client
from multiprocessing import Process

def run_node(n):
	n.start()

if __name__ == '__main__':
	nodes = []
	idx2peer = {1: ('0.0.0.0', 8003), 2: ('0.0.0.0', 8004), 3: ('0.0.0.0', 8005)}
	t = 1
	n = 3
	for i in range(1, n+1):
		nodes.append(Node(7999+i, t, n, i, idx2peer))
	try:
		for node in nodes:
			node.start_mpc_server()
		for node in nodes:
			node.start_mpc_clients()
		procs = []
		for node in nodes:
			procs.append(Process(target=run_node, args=(node,)))
		for p in procs:
			p.start()
		for p in procs:
			p.join()
	finally:
		for node in nodes:
			node.stop_mpc_clients()
		for node in nodes:
			node.stop_mpc_server()



