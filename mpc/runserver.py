from server import Server

if __name__ == '__main__':
	import sys
	args = sys.argv[1:]
	bootstrap=[]
	if len(args) > 4:
		bootstrap = eval(args[4])
	s = Server(int(args[0]), int(args[1]), int(args[2]), int(args[3]), bootstrap=bootstrap)
	s.start()