<<<<<<< HEAD
from circuit import Circuit
import asyncio

def test_cleartext_add64():
=======
from circuit import Circuit, RuntimeCircuit
import time

def test_cleartext_add64():
	c = Circuit("bristol_circuits/add64.txt", ['V' for _ in range(128)])
>>>>>>> upstream/master
	for x,y in [(1000, 2010), (100, 200), (111111, 23456), (2**32-1, 2**32-1), (2**60, 2**60+5), (2**63, 2**63+1), (2**64-25, 2**64-100), (2**64-1, 2**64-1)]:
		answer = (x+y)%(2**64)

		x_bits = [int(c) for c in bin(x)[2:]]
		if len(x_bits)<64:
			x_bits = [0 for _ in range(64 - len(x_bits))]+ x_bits

		y_bits = [int(c) for c in bin(y)[2:]]
		if len(y_bits)<64:
			y_bits = [0 for _ in range(64 - len(y_bits))]+ y_bits
		x_bits = list(reversed(x_bits))
		y_bits = list(reversed(y_bits))
<<<<<<< HEAD
		c = Circuit("bristol_circuits/add64.txt", ['V' for _ in range(128)])
		out_bits = asyncio.run(c.evaluate(x_bits+y_bits))
=======
		out_bits = RuntimeCircuit(c, x_bits+y_bits).evaluate()
>>>>>>> upstream/master
		out_string = ''.join([str(i) for i in list(reversed(out_bits))])
		assert eval('0b'+out_string) == answer, "computed wrong value"

def test_cleartext_sub64():
<<<<<<< HEAD
=======
	c = Circuit("bristol_circuits/sub64.txt", ['V' for _ in range(128)])
>>>>>>> upstream/master
	for x,y in [(1000, 2010), (2010, 1000), (2**32-1, 2**32-1), (2**60, 2**60+5), (2**63, 2**63+1), (2**64-25, 2**64-100), (2**64-1, 2**64-1)]:
		answer = (x-y)%(2**64)

		x_bits = [int(c) for c in bin(x)[2:]]
		if len(x_bits)<64:
			x_bits = [0 for _ in range(64 - len(x_bits))]+ x_bits

		y_bits = [int(c) for c in bin(y)[2:]]
		if len(y_bits)<64:
			y_bits = [0 for _ in range(64 - len(y_bits))]+ y_bits
		x_bits = list(reversed(x_bits))
		y_bits = list(reversed(y_bits))
<<<<<<< HEAD
		c = Circuit("bristol_circuits/sub64.txt", ['V' for _ in range(128)])
		out_bits = asyncio.run(c.evaluate(x_bits+y_bits))
=======
		out_bits = RuntimeCircuit(c, x_bits+y_bits).evaluate()
>>>>>>> upstream/master
		out_string = ''.join([str(i) for i in list(reversed(out_bits))])
		assert eval('0b'+out_string) == answer, "computed wrong value"

def test_cleartext_mul64mod():
<<<<<<< HEAD
=======
	c = Circuit("bristol_circuits/mul64mod.txt", ['V' for _ in range(128)])
>>>>>>> upstream/master
	for x,y in [(100, 200), (111111, 23456), (2**30, 2**10), (2**63, 2**63+1), (2**64-1, 2**64-1)]:
		answer = (x*y)%(2**64)

		x_bits = [int(c) for c in bin(x)[2:]]
		if len(x_bits)<64:
			x_bits = [0 for _ in range(64 - len(x_bits))]+ x_bits

		y_bits = [int(c) for c in bin(y)[2:]]
		if len(y_bits)<64:
			y_bits = [0 for _ in range(64 - len(y_bits))]+ y_bits
		x_bits = list(reversed(x_bits))
		y_bits = list(reversed(y_bits))
<<<<<<< HEAD
		c = Circuit("bristol_circuits/mul64mod.txt", ['V' for _ in range(128)])
		out_bits = asyncio.run(c.evaluate(x_bits+y_bits))
=======
		out_bits = RuntimeCircuit(c, x_bits+y_bits).evaluate()
>>>>>>> upstream/master
		out_string = ''.join([str(i) for i in list(reversed(out_bits))])
		assert eval('0b'+out_string) == answer, "computed wrong value"

def test_cleartext_mul64():
<<<<<<< HEAD
=======
	c = Circuit("bristol_circuits/mul64.txt", ['V' for _ in range(128)])
>>>>>>> upstream/master
	for x,y in [(100, 200), (111111, 23456), (2**30, 2**10), (2**63, 2**63+1), (2**64-1, 2**64-1)]:
		answer = x*y

		x_bits = [int(c) for c in bin(x)[2:]]
		if len(x_bits)<64:
			x_bits = [0 for _ in range(64 - len(x_bits))]+ x_bits

		y_bits = [int(c) for c in bin(y)[2:]]
		if len(y_bits)<64:
			y_bits = [0 for _ in range(64 - len(y_bits))]+ y_bits
		x_bits = list(reversed(x_bits))
		y_bits = list(reversed(y_bits))
<<<<<<< HEAD
		c = Circuit("bristol_circuits/mul64.txt", ['V' for _ in range(128)])
		out_bits = asyncio.run(c.evaluate(x_bits+y_bits))
=======
		out_bits = RuntimeCircuit(c, x_bits+y_bits).evaluate()
>>>>>>> upstream/master
		out_string = ''.join([str(i) for i in list(reversed(out_bits))])
		out_string = out_string[64:]+out_string[:64]
		assert eval('0b'+out_string) == answer, "computed wrong value"

def test_cleartext_lessthan32():
<<<<<<< HEAD
=======
	c = Circuit("bristol_circuits/lessthan32.txt", ['V' for _ in range(64)])
>>>>>>> upstream/master
	for x,y in [(100, 200), (200, 100), (111111, 23456), (2**30, 2**10), (2**10, 2**30), (2**32-1, 2**32-1)]:
		answer = 1 if x<y else 0

		x_bits = [int(c) for c in bin(x)[2:]]
		if len(x_bits)<32:
			x_bits = [0 for _ in range(32 - len(x_bits))]+ x_bits

		y_bits = [int(c) for c in bin(y)[2:]]
		if len(y_bits)<32:
			y_bits = [0 for _ in range(32 - len(y_bits))]+ y_bits
		x_bits = list(reversed(x_bits))
		y_bits = list(reversed(y_bits))
<<<<<<< HEAD
		c = Circuit("bristol_circuits/lessthan32.txt", ['V' for _ in range(64)])
		out_bit = asyncio.run(c.evaluate(x_bits+y_bits))
=======
		out_bit = RuntimeCircuit(c, x_bits+y_bits).evaluate()
>>>>>>> upstream/master
		assert out_bit[0] == answer, "computed wrong value"

def test_cleartext_dist32():
	x = 4060000
	y = 7390000
	cx = 4063500
	cy = 7396000
	rsq = 64000000
	answer = 1 if ((x-cx)**2 + (y-cy)**2) < rsq else 0

	inputs = [0 for _ in range(32)]
	x_bits = [int(b) for b in bin(x)[2:]]
	if len(x_bits)<32:
		x_bits = [0 for _ in range(32 - len(x_bits))]+ x_bits
	y_bits = [int(b) for b in bin(y)[2:]]
	if len(y_bits)<32:
		y_bits = [0 for _ in range(32 - len(y_bits))]+ y_bits
	cx_bits = [int(b) for b in bin(cx)[2:]]
	if len(cx_bits)<32:
		cx_bits = [0 for _ in range(32 - len(cx_bits))]+ cx_bits
	cy_bits = [int(b) for b in bin(cy)[2:]]
	if len(cy_bits)<32:
		cy_bits = [0 for _ in range(32 - len(cy_bits))]+ cy_bits
	rsq_bits = [int(b) for b in bin(rsq)[2:]]
	if len(rsq_bits)<32:
		rsq_bits = [0 for _ in range(32 - len(rsq_bits))]+ rsq_bits
	inputs.extend(x_bits[::-1])
	inputs.extend(y_bits[::-1])
	inputs.extend(cx_bits[::-1])
	inputs.extend(cy_bits[::-1])
	inputs.extend(rsq_bits[::-1])
	c = Circuit("bristol_circuits/dist32.txt", ['V' for _ in range(192)])
<<<<<<< HEAD
	out_bit = asyncio.run(c.evaluate(inputs))
	assert out_bit[0] == answer, "computed wrong value"

def test_cleartext_addsub_example():
	x = 1000
	y = 2000
	answer1 = (x+y)%(2**64)
	answer2 = (x-y)%(2**64)

	x_bits = [int(c) for c in bin(x)[2:]]
	if len(x_bits)<64:
		x_bits = [0 for _ in range(64 - len(x_bits))]+ x_bits

	y_bits = [int(c) for c in bin(y)[2:]]
	if len(y_bits)<64:
		y_bits = [0 for _ in range(64 - len(y_bits))]+ y_bits
	x_bits = list(reversed(x_bits))
	y_bits = list(reversed(y_bits))
	c = Circuit("bristol_circuits/example.txt", ['V' for _ in range(128)])
	out_bits = asyncio.run(c.evaluate(x_bits+y_bits))
	out_string = ''.join([str(i) for i in list(reversed(out_bits))])
	assert eval('0b'+out_string[:64]) == answer2, "computed wrong value"
	assert eval('0b'+out_string[64:]) == answer1, "computed wrong value"

def test_cleartext_unnormalized_subregion_example():
	answer = 300

	inputs = [0 for _ in range(64)] + [1 for _ in range(1200)]

	c = Circuit("bristol_circuits/unnormalized_subregion_100_10.txt", ['V' for _ in range(1264)])
	out_bits = asyncio.run(c.evaluate(inputs))
	out_string = ''.join([str(i) for i in list(reversed(out_bits))])
	for i in range(10):
		assert eval('0b'+out_string[i*64: (i+1)*64]) == answer, "computed wrong value"

if __name__ == "__main__":
=======
	out_bit = RuntimeCircuit(c, inputs).evaluate()
	assert out_bit[0] == answer, "computed wrong value"

def test_cleartext_unnormalized_subregion_10k():
	start = time.time()
	c = Circuit("bristol_circuits/unnormalized_subregion_10000_1.txt", ['V' for _ in range(30064)])
	print(f"circuit load time: {round(time.time()-start, 4)}")
	answer = 30000
	inputs = [0 for _ in range(64)] + [1 for _ in range(30000)]
	start = time.time()
	out_bits = RuntimeCircuit(c, inputs).evaluate()
	out_string = ''.join([str(i) for i in list(reversed(out_bits))])
	assert eval('0b'+out_string) == answer, "computed wrong value"
	print(f"PASS, time: {round(time.time()-start, 4)}")
	answer = 5000
	inputs = [0 for _ in range(64)]
	for i in range(10000):
		if i%2==0:
			inputs.extend([1,0,1])
		else:
			inputs.extend([1,0,0])
	start = time.time()
	out_bits = RuntimeCircuit(c, inputs).evaluate()
	out_string = ''.join([str(i) for i in list(reversed(out_bits))])
	assert eval('0b'+out_string) == answer, "computed wrong value"
	print(f"PASS, time: {round(time.time()-start, 4)}")
	answer = 7500
	inputs = [0 for _ in range(64)]
	for i in range(10000):
		if i%4==0:
			inputs.extend([1,1,1])
		else:
			inputs.extend([1,1,0])
	start = time.time()
	out_bits = RuntimeCircuit(c, inputs).evaluate()
	out_string = ''.join([str(i) for i in list(reversed(out_bits))])
	assert eval('0b'+out_string) == answer, "computed wrong value"
	print(f"PASS, time: {round(time.time()-start, 4)}")

if __name__ == "__main__":
	print("--TEST BASIC CIRCUITS--")
>>>>>>> upstream/master
	test_cleartext_add64()
	test_cleartext_sub64()
	test_cleartext_mul64mod()
	test_cleartext_mul64()
	test_cleartext_lessthan32()
	test_cleartext_dist32()
<<<<<<< HEAD
	test_cleartext_addsub_example()
	test_cleartext_unnormalized_subregion_example()
	print("PASS")
=======
	print("PASS")
	print("--TEST SUBREGION CIRCUIT--")
	test_cleartext_unnormalized_subregion_10k()
	print("ALL TESTS PASSED")
>>>>>>> upstream/master
	