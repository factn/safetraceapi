from circuit import Circuit

def test_cleartext_circuit():
	x = 20000
	y = 200
	answer = x*y

	x_bits = [int(c) for c in bin(x)[2:]]
	if len(x_bits)<32:
		x_bits = [0 for _ in range(32 - len(x_bits))]+ x_bits

	y_bits = [int(c) for c in bin(y)[2:]]
	if len(y_bits)<32:
		y_bits = [0 for _ in range(32 - len(y_bits))]+ y_bits

	c = Circuit("circuits/mul32_circuit.txt", ['V' for _ in range(64)])
	out_bits = c.evaluate(x_bits+y_bits)
	out_string = ''.join([str(i) for i in out_bits])
	print(eval('0b'+out_string) == answer)

if __name__ == "__main__":
	test_cleartext_circuit()
	print("PASS")
