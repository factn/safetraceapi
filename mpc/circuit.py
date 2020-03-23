class Circuit:

	def __init__(self, path):
		with open(path, "r") as f:
			text = f.read()
		lines = text.split("\n")
		self.circuit = [i.split() for i in lines]

	def run(self, inputs):
		tape = [0,1]+inputs
		outputs = [None for _ in range(len([i for i in self.circuit if "OUT" in i]))]
		for gate in self.circuit:
			if gate == []:
				pass
			elif gate[-1] == 'XOR':
				tape.append(self.XOR(tape[int(gate[-2])], tape[int(gate[-3])]))
			elif gate[-1] == 'AND':
				tape.append(self.AND(tape[int(gate[-2])], tape[int(gate[-3])]))
			elif gate[-1] == "OUT":
				outputs[int(gate[-2])] = tape[int(gate[-3])]
		return outputs

	def XOR(self, a, b):
		return a^b

	def AND(self, a, b):
		return a&b