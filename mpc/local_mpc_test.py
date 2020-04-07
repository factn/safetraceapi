# NOTE: MUST run local_mpc_network.py in a separate process for this test to work
from client import Client
import asyncio, random, time

async def test_mpc_intersection(clients, number):
	pid = ''.join([random.choice([i for i in 'abcdef123456789']) for _ in range(10)])
	nums = [random.choice(range(1,3001)) for _ in range(2)]
	result = 0
	if (nums[0]-nums[1])**2 < 1000**2:
		result = 1
	start = time.time()
	tasks = [clients[i].operation(nums[i], pid) for i in range(2)]
	answers = await asyncio.gather(*tasks)
	took = round(time.time()-start, 4)
	for a in answers:
		assert int(a) == result, "reconstructed wrong result"
	print(f"PASS intersection {number}, time: {took}")

if __name__ == '__main__':
	# NOTE: MUST run local_mpc_network.py in a separate process for this test to work
	idx2node={1: ('0.0.0.0', 8000), 2: ('0.0.0.0', 8001), 3: ('0.0.0.0', 8002)}
	clients = [Client(1,3, idx2node) for _ in range(2)]
	for i in range(3):
		asyncio.run(test_mpc_intersection(clients, i+1))


