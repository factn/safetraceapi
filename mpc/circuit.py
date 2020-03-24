from shamir import Share

class Circuit:

	def __init__(self, path):
		with open(path, "r") as f:
			text = f.read()
		lines = text.split("\n")
		self.circuit = [i.split() for i in lines]

	def evaluate(self, inputs, shamir=None, messenger=None, triples=None):
		self.shamir = shamir
		self.messenger = messenger
		self.triples = triples
		self.round = 0
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
		if (type(a) == Share) and (type(b) == Share):
			return a+b
		elif (a in [0,1]) and (a in [0,1]):
			return a^b
		elif (a in [0,1]) and (type(b) == Share):
			return b.scalar_shift(a)
		elif (b in [0,1]) and (type(a) == Share):
			return a.scalar_shift(b)


	def AND(self, a, b):
		if (type(a) == Share) and (type(b) == Share):
			## COMMUNICATION
			self.round += 1
			triple = self.triples.pop(0)
			data = self.shamir.multiply_shars_round_1(a, b, triple)
			self.messenger.broadcast(self.round, data)
			resps = self.messenger.collect(self.round)
			return self.shamir.multiply_shars_round_2(a, b, [r[0] for r in resps], [r[1] for r in resps], triple.c)
		elif (a in [0,1]) and (b in [0,1]):
			return a&b
		elif (a in [0,1]) and (type(b) == Share):
			return b.scalar_mul(a)
		elif (b in [0,1]) and (type(a) == Share):
			return a.scalar_mul(b)