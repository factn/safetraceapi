from mpc import MPCPeer
from ecies.utils import generate_key

if __name__ == '__main__':
	import sys
	args = sys.argv[1:]
	bootstrap=[]
	if len(args) > 4:
		bootstrap = eval(args[4])
	if len(args) > 5:
		key = args[5]
	else:
		key = generate_key().to_hex()
	if len(args) > 6:
		endpoint = args[6]
	else:
		endpoint = None
	if len(args) > 7:
		api_key = args[7]
	else:
		api_key = None
	peer = MPCPeer(int(args[0]), int(args[1]), int(args[2]), int(args[3]), key, bootstrap, 'TRIPLE', api_endpoint=endpoint, api_key=api_key)
	peer.start()