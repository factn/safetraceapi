# NOTE: MUST run local_mpc_network.py in a separate process for this test to work
from client import Client
import asyncio, random, time

async def test_mpc_intersection(client, i):
	pid = ''.join([random.choice([i for i in 'abcdef123456789']) for _ in range(10)])
	c_x = 40.63500
	c_y = -73.96000
	bcx = round((c_x+90)*100000)
	bcy = round((c_y+180)*100000)
	x = random.choice(range(bcx-12000, bcx+12000)) # slightly larger than query radius
	y = random.choice(range(bcy-12000, bcy+12000)) # slightly larger than query radius
	result = 0
	if (x-bcx)**2 + (y-bcy)**2 < 8000**2:
		result = 1
	start = time.time()
	answer = await client.operation(x, y, pid)
	took = round(time.time()-start, 4)
	assert int(answer) == result, "reconstructed wrong result"
	if result == 1:
		print(f"PASS {i}, time: {took} (in region)")
	else:
		print(f"PASS {i}, time: {took} (not in region)")

async def test_concurrent_mpc_ops(clients, j):
	tasks = []
	for k in range(len(clients)):
		tasks.append(test_mpc_intersection(clients[j], (len(clients)*j)+k))
	await asyncio.gather(*tasks)

if __name__ == '__main__':
	# NOTE: MUST run local_mpc_network.py in a separate process for this test to work
	n_simultaneous_queries = 3
	idx2node={1: ('0.0.0.0', 8000), 2: ('0.0.0.0', 8001), 3: ('0.0.0.0', 8002)}
	client = Client(1,3, idx2node)
	start = time.time()
	for j in range(3):
		asyncio.run(test_mpc_intersection(client, j))
	print(f"ALL TESTS PASSED, total time: {round(time.time()-start, 4)}")
