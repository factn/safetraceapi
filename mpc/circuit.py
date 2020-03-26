from shamir import Share

class Circuit:

	def __init__(self, path, input_types):
		with open(path, "r") as f:
			text = f.read()
		lines = text.split("\n")
		n_inputs = int(lines[0])
		assert n_inputs == len(input_types), "first line of circuit must match number of inputs"
		tape = [(('V', 0, False), None), (('V', 0, False), None)]
		outputs = [None for _ in range(len([i for i in lines if "OUT" in i]))]
		for i in input_types:
			tape.append(((i, 0, False), None))
		n_layers = 0
		for l in lines[1:]:
			words = l.split()
			if words == []:
				continue
			in1 = tape[int(words[-2])]
			in2 = tape[int(words[-3])]
			layer1 = in1[0][1]
			if in1[0][2]:
				layer1 += 1
			layer2 = in2[0][1]
			if in2[0][2]:
				layer2 += 1
			layer = max(layer1, layer2)
			n_layers = max(n_layers, layer)
			if words[-1] == 'AND':
				if (in1[0][0] == 'S') and (in2[0][0] == 'S'):
					tape.append((('S', layer, True), words))
				elif (in1[0][0] == 'S') or (in2[0][0] == 'S'):
					tape.append((('S', layer, False), words))
				elif (in1[0][0] == 'V') and (in2[0][0] == 'V'):
					tape.append((('V', layer, False), words))
				else:
					raise ValueError("AND gate improperly formatted")
			elif words[-1] == 'XOR':
				if (in1[0][0] == 'S') or (in2[0][0] == 'S'):
					tape.append((('S', layer, False), words))
				elif (in1[0][0] == 'V') and (in2[0][0] == 'V'):
					tape.append((('V', layer, False), words))
				else:
					raise ValueError("XOR gate improperly formatted")
			elif words[-1] == 'OUT':
				outputs[int(words[-2])] = int(words[-3])
			else:
				raise ValueError("Improperly formatted circuit")
		self.output_indexes = outputs
		self.circuit_layers = [[] for _ in range(n_layers+1)]
		self.tape_len = len(tape)
		for i in range(self.tape_len):
			if tape[i][1] != None:
				self.circuit_layers[tape[i][0][1]].append((i, tape[i][0][2], tape[i][1]))

	def evaluate(self, inputs, shamir=None, messenger=None, triples=None):
		tape = [None for _ in range(self.tape_len)]
		tape[0] = 0
		tape[1] = 1
		for i in range(len(inputs)):
			tape[i+2] = inputs[i]
		for i in range(len(self.circuit_layers)):
			layer = self.circuit_layers[i]
			x_shares = []
			y_shares = []
			indexes = []
			for gate in layer:
				if not gate[1]:
					if gate[2][-1] == 'XOR':
						tape[gate[0]] = self.XOR(tape[int(gate[2][-2])], tape[int(gate[2][-3])])
					elif gate[2][-1] == 'AND':
						tape[gate[0]] = self.AND(tape[int(gate[2][-2])], tape[int(gate[2][-3])])
					else:
						raise ValueError(f"Improperly formatted gate: {gate}")
				else:
					indexes.append(gate[0])
					x_shares.append(tape[int(gate[2][-3])])
					y_shares.append(tape[int(gate[2][-2])])
			if len(indexes) > 0:
				t = triples[0:len(indexes)]
				triples = triples[len(indexes):]
				msg = shamir.mul_gates_round_1(x_shares, y_shares, t)
				messenger.broadcast(i, msg)
				resps = messenger.collect(i)
				vals = shamir.mul_gates_round_2(x_shares, y_shares, resps, [j.c for j in t])
				for k in range(len(indexes)):
					tape[indexes[k]] = vals[k]
		return [tape[k] for k in self.output_indexes]

	def XOR(self, a, b):
		if (type(a) == Share) and (type(b) == Share):
			return a+b
		elif (a in [0,1]) and (b in [0,1]):
			return a^b
		elif (a in [0,1]) and (type(b) == Share):
			return b.scalar_shift(a)
		elif (b in [0,1]) and (type(a) == Share):
			return a.scalar_shift(b)
		else:
			raise ValueError(f"Inputs do not match XOR gate: {(a, type(a)), (b, type(b))}")

	def AND(self, a, b):
		if (a in [0,1]) and (b in [0,1]):
			return a&b
		elif (a in [0,1]) and (type(b) == Share):
			return b.scalar_mul(a)
		elif (b in [0,1]) and (type(a) == Share):
			return a.scalar_mul(b)
		else:
			raise ValueError(f"Inputs do not match AND gate: {(a, type(a)), (b, type(b))}")
