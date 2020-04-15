from client import Client
from multiprocessing import Process
import asyncio, random, time, subprocess

async def test_mpc_intersection(client, i):
	pid = ''.join([random.choice([i for i in 'abcdef123456789']) for _ in range(10)])
	c_x = 40.63500
	c_y = -73.96000
	bcx = round((c_x+90)*100000)
	bcy = round((c_y+180)*100000)
	x = random.choice(range(bcx-12000, bcx+12000))
	y = random.choice(range(bcy-12000, bcy+12000)) 
	result = 0
	if (x-bcx)**2 + (y-bcy)**2 < 8000**2:
		result = 1
	start = time.time()
	answer = await client.intersection_operation(x, y, pid)
	took = round(time.time()-start, 4)
	assert int(answer) == result, "reconstructed wrong result"
	if result == 1:
		print(f"PASS {i}, time: {took} (in region)")
	else:
		print(f"PASS {i}, time: {took} (not in region)")

async def test_concurrent_mpc_ops(clients, j):
	tasks = []
	for k in range(len(clients)):
		tasks.append(test_mpc_intersection(clients[k], (len(clients)*j)+k))
	await asyncio.gather(*tasks)

def run_node(args):
	subprocess.call(args)

if __name__ == '__main__':
	# kill any running processes
	t = 1
	n = 3
	for j in range(8000, 8000+n+1):
		try:
			pids = subprocess.check_output(['lsof', '-t',  '-i',  f':{j}']).decode().split('\n')
			pids = [p for p in pids if p != '']
			print(pids)
			for o in pids:
				subprocess.call(['kill', '-9', f'{o}'])
		except:
			pass
	# start mpc servers
	print('bootstrapping mpc network...')
	cmd = "python3 runserver.py"
	bootstrap = [("127.0.0.1", 7999+i, i) for i in range(1, n+1)]
	procs = []
	for i in range(1, n+1):
		node_bootstrap = [b for b in bootstrap if b[2] != i]
		node_args = (cmd + f' {7999+i} {t} {n} {i}').split()
		node_args.append(repr(node_bootstrap))
		procs.append(Process(target=run_node, args=(node_args,)))
	for p in procs:
		p.start()
	time.sleep(2.5)
	# run tests
	n_simultaneous_queries = 3
	idx2node={i: ('0.0.0.0', 7999+i) for i in range(1, n+1)}
	clients = [Client(t, n, idx2node) for _ in range(n_simultaneous_queries)]
	start = time.time()
	for i in range(2):
		asyncio.run(test_concurrent_mpc_ops(clients, i))
	print(f"ALL TESTS PASSED, total time: {round(time.time()-start, 4)}")
	for p in procs:
		p.terminate()
