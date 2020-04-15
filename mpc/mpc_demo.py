from client import Client
import random, sys

'''
Pass any geo-coordinates in the Northern Hemisphere of the globe and the
mpc servers will compute whether or not the coordinate is in Brooklyn, NY
IN ZERO KNOWLEDGE (without ever leaking any other information about the coordinate).

Example call:

$ python3 mpc_demo.py -lat 40.6350 -lon -73.95 

(this should return a 1, because that's in Brooklyn!)
'''

if __name__ == '__main__':
	argv = sys.argv[1:]
	x = None
	y = None
	for i in range(len(argv)):
		if argv[i] == '-lat' and len(argv)>i+1:
			x = float(argv[i+1])
		if argv[i] == '-lon' and len(argv)>i+1:
			y = float(argv[i+1])
	if x == None or y == None:
		raise ValueError('must pass a geolocal coordinate using -lat and -lon options')
	if x > 90 or x < -1*90:
		raise ValueError('invalid latitude (must be between +/- 90 in decimal degree notation')
	if y > 180 or y < -1*180:
		raise ValueError('invalid longitude (must be within +/- 180 in decimal degree notation)')
	x = round((x + 90)*100000) # shift to 0-180
	y = round((y + 180)*100000) # shift to 0-360
	idx2node = {i: ('54.237.244.61', 7999+i) for i in range(1,4)}
	pid = ''.join([random.choice([i for i in 'abcdef123456789']) for _ in range(10)])
	c = Client(1, 3, idx2node)
	print(c.do_intersection_operation(x, y, pid))
