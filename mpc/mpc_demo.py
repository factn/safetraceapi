from client import Client

'''
Pass an integer below 18 trillion and any reference id as two command line args:

$ python3 mpc_demo.py 1000 abcd

if someone else (or you in a separate process) runs the same script with the same reference id for example:

$ python3 mpc_demo.py 15000000 abcd

Then the remote servers will securely compute the intersection. Without ever decrypting the two private inputs (the integers) 
the clients can learn if their two integers were more than or less than 1000 units away from one another (1 for intersect, 0 otherwise).
The servers don't know the inputs or even the result of the computation, which is locally reconstructed client side from the server shares.
'''

if __name__ == '__main__':
	import sys

	args = sys.argv[1:]

	idx2node = {i: ('54.237.244.61', 7999+i) for i in range(1,4)}
	c = Client(1, 3, idx2node)
	print(c.send_operation(int(args[0]), args[1]))
