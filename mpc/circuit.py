from shamir import Share

class Circuit:

	def __init__(self, path, input_types):
		with open(path, "r") as f:
			data = f.read()
		circuit, n_layers, outputs = self.__load_bristol_circuit(data, input_types)
		self.output_indexes = outputs
		self.circuit_layers = [[] for _ in range(n_layers+1)]
		lines = [k for k in data.split("\n")[4:] if 'EQW' not in k]
		order = [int(i.split()[-2])+2 for i in lines]
		self.tape_len = max(order)+1
		for i in order:
			gate = circuit[i]
			if gate[1] != None:
				self.circuit_layers[gate[0][1]].append((i, gate[0][2], gate[1]))

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
						tape[gate[0]] = self.__XOR(tape[gate[2][-2]], tape[gate[2][-3]])
					elif gate[2][-1] == 'AND':
						tape[gate[0]] = self.__AND(tape[gate[2][-2]], tape[gate[2][-3]])
					else:
						raise ValueError(f"Improperly formatted gate: {gate}")
				else:
					indexes.append(gate[0])
					x_shares.append(tape[gate[2][-3]])
					y_shares.append(tape[gate[2][-2]])
			if len(indexes) > 0:
				trips = triples[:len(indexes)]
				triples = triples[len(indexes):]
				msg = shamir.mul_gates_round_1(x_shares, y_shares, trips)
				messenger.broadcast("MUL", i, msg)
				resps = messenger.collect(i)
				resps.append(msg)
				vals = shamir.mul_gates_round_2(x_shares, y_shares, resps, [j.c for j in trips])
				for k in range(len(indexes)):
					tape[indexes[k]] = vals[k]
		return [tape[k] for k in self.output_indexes]

	def __XOR(self, a, b):
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

	def __AND(self, a, b):
		if (a in [0,1]) and (b in [0,1]):
			return a&b
		elif (a in [0,1]) and (type(b) == Share):
			return b.scalar_mul(a)
		elif (b in [0,1]) and (type(a) == Share):
			return a.scalar_mul(b)
		else:
			raise ValueError(f"Inputs do not match AND gate: {(a, type(a)), (b, type(b))}")

	def __load_bristol_circuit(self, data, input_types):
		lines = data.split("\n")
		last_index = int(lines[0].split()[-1])
		inputs = [int(i) for i in lines[1].split() if i!='']
		outputs = [int(i) for i in lines[2].split() if i!='']
		n_inputs = inputs[1] if len(inputs)==2 else inputs[1]+inputs[2]
		n_outputs = outputs[1] if len(outputs)==2 else outputs[1]+outputs[2]
		output_indexes = list(range(last_index-n_outputs+2, last_index+2))
		lines = lines[4:]
		assert n_inputs == len(input_types), "first line of circuit must match number of inputs"
		tape = {0: (('V', 0, False), None), 1:(('V', 0, False), None)}
		for i in range(len(input_types)):
			tape[i+2] = ((input_types[i], 0, False), None)
		n_layers = 0
		for l in lines:
			words = l.split()
			if words == []:
				pass		
			elif words[-1] == 'EQW':
				for i in range(len(outputs)):
					if outputs[i] == int(words[-2])+2:
						outputs[i] = int(words[-3])+2
			elif words[-1] == 'AND':
				in1 = tape[int(words[-3])+2]
				layer1 = in1[0][1]
				if in1[0][2]:
					layer1 += 1
				in2 = tape[int(words[-4])+2]
				layer2 = in2[0][1]
				if in2[0][2]:
					layer2 += 1
				layer = max(layer1, layer2)
				n_layers = max(n_layers, layer)
				if (in1[0][0] == 'S') and (in2[0][0] == 'S'):
					tape[int(words[-2])+2] = (('S', layer, True), (int(words[-4])+2, int(words[-3])+2, words[-1]))
				elif (in1[0][0] == 'S') or (in2[0][0] == 'S'):
					tape[int(words[-2])+2] = (('S', layer, False), (int(words[-4])+2, int(words[-3])+2, words[-1]))
				elif (in1[0][0] == 'V') and (in2[0][0] == 'V'):
					tape[int(words[-2])+2] = (('V', layer, False), (int(words[-4])+2, int(words[-3])+2, words[-1]))
				else:
					raise ValueError("AND gate improperly formatted")
			elif words[-1] == 'XOR':
				in1 = tape[int(words[-3])+2]
				layer1 = in1[0][1]
				if in1[0][2]:
					layer1 += 1
				in2 = tape[int(words[-4])+2]
				layer2 = in2[0][1]
				if in2[0][2]:
					layer2 += 1
				layer = max(layer1, layer2)
				n_layers = max(n_layers, layer)
				if (in1[0][0] == 'S') or (in2[0][0] == 'S'):
					tape[int(words[-2])+2] = (('S', layer, False), (int(words[-4])+2, int(words[-3])+2, words[-1]))
				elif (in1[0][0] == 'V') and (in2[0][0] == 'V'):
					tape[int(words[-2])+2] = (('V', layer, False), (int(words[-4])+2, int(words[-3])+2, words[-1]))
				else:
					raise ValueError("XOR gate improperly formatted")
			elif words[-1] == "INV":
				in1 = tape[int(words[-3])+2]
				layer = in1[0][1]
				if in1[0][2]:
					layer += 1
				n_layers = max(n_layers, layer)
				tape[int(words[-2])+2] = ((in1[0][0], layer, False), (int(words[-3])+2, 1, 'XOR'))
			else:
				raise ValueError("Improperly formatted circuit")
		return tape, n_layers, output_indexes
