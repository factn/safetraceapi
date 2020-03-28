from circuit import Circuit

def test_cleartext_add64():
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
		c = Circuit("bristol_circuits/add64.txt", ['V' for _ in range(128)])
		out_bits = c.evaluate(x_bits+y_bits)
		out_string = ''.join([str(i) for i in list(reversed(out_bits))])
		assert eval('0b'+out_string) == answer, "computed wrong value"

def test_cleartext_sub64():
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
		c = Circuit("bristol_circuits/sub64.txt", ['V' for _ in range(128)])
		out_bits = c.evaluate(x_bits+y_bits)
		out_string = ''.join([str(i) for i in list(reversed(out_bits))])
		assert eval('0b'+out_string) == answer, "computed wrong value"

def test_cleartext_mul64mod():
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
		c = Circuit("bristol_circuits/mul64mod.txt", ['V' for _ in range(128)])
		out_bits = c.evaluate(x_bits+y_bits)
		out_string = ''.join([str(i) for i in list(reversed(out_bits))])
		assert eval('0b'+out_string) == answer, "computed wrong value"

def test_cleartext_mul64():
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
		c = Circuit("bristol_circuits/mul64.txt", ['V' for _ in range(128)])
		out_bits = c.evaluate(x_bits+y_bits)
		out_string = ''.join([str(i) for i in list(reversed(out_bits))])
		out_string = out_string[64:]+out_string[:64]
		assert eval('0b'+out_string) == answer, "computed wrong value"

def test_cleartext_lessthan32():
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
		c = Circuit("bristol_circuits/lessthan32.txt", ['V' for _ in range(64)])
		out_bit = c.evaluate(x_bits+y_bits)
		assert out_bit[0] == answer, "computed wrong value"

if __name__ == "__main__":
	test_cleartext_add64()
	test_cleartext_sub64()
	test_cleartext_mul64mod()
	test_cleartext_mul64()
	test_cleartext_lessthan32()
	print("PASS")
