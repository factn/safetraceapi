from server import Server
from client import Client
from multiprocessing import Process
import subprocess

def run_node(n):
	n.start()

if __name__ == '__main__':
	# kill any running processes
	for j in range(8000, 8006):
		try:
			pids = subprocess.check_output(['lsof', '-t',  '-i',  f':{j}']).decode().split('\n')
			pids = [p for p in pids if p != '']
			print(pids)
			for o in pids:
				subprocess.call(['kill', '-9', f'{o}'])
		except:
			pass
	# run nodes
	nodes = []
	idx2peer = {1: ('0.0.0.0', 8003), 2: ('0.0.0.0', 8004), 3: ('0.0.0.0', 8005)}
	t = 1
	n = 3
	for i in range(1, n+1):
		nodes.append(Server(7999+i, t, n, i, idx2peer))
	try:
		for node in nodes:
			node.start_mpc_server()
		for node in nodes:
			node.start_mpc_client()
		procs = []
		for node in nodes:
			procs.append(Process(target=run_node, args=(node,)))
		for p in procs:
			p.start()
		for p in procs:
			p.join()
	finally:
		for node in nodes:
			node.stop_mpc_client()
		for node in nodes:
			node.stop_mpc_server()



