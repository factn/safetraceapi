from shamir import Share

class RuntimeCircuit:

	def __init__(self, circuit, inputs, triples=None, shamir=None):
		self.circuit_layers = circuit.circuit_layers
		self.tape_len = circuit.tape_len
		self.output_indexes = circuit.output_indexes
		self.tape = [None for _ in range(self.tape_len)]
		self.tape[0] = 0
		self.tape[1] = 1
		for i in range(len(inputs)):
			self.tape[i+2] = inputs[i]
		self.triples = triples
		self.shamir = shamir

	def compute_layer(self, i):
		layer = self.circuit_layers[i]
		x_shares = []
		y_shares = []
		indexes = [gate[0] for gate in layer if gate[1]==True]
		for gate in layer:
			if not gate[1]:
				if gate[2][-1] == 'XOR':
					self.tape[gate[0]] = self.__XOR(self.tape[gate[2][-2]], self.tape[gate[2][-3]])
				elif gate[2][-1] == 'AND':
					self.tape[gate[0]] = self.__AND(self.tape[gate[2][-2]], self.tape[gate[2][-3]])
				else:
					raise ValueError(f"Improperly formatted gate: {gate}")
			else:
				x_shares.append(self.tape[gate[2][-3]])
				y_shares.append(self.tape[gate[2][-2]])
		msg = None
		round_ts = []
		if len(indexes) > 0:
			round_ts = self.triples[:len(indexes)]
			self.triples = self.triples[len(indexes):]
			msg = self.shamir.mul_gates_round_1(x_shares, y_shares, round_ts)	
		return indexes, x_shares, y_shares, msg, [t.c for t in round_ts]

	def finish_layer(self, indexes, x_shares, y_shares, msgs, cs):
		vals = self.shamir.mul_gates_round_2(x_shares, y_shares, msgs, cs)
		for k in range(len(indexes)):
			self.tape[indexes[k]] = vals[k]

	def get_outputs(self):
		return [self.tape[i] for i in self.output_indexes]

	def evaluate(self, mock_messenger=None):
		for i in range(len(self.circuit_layers)):
			print(f"BEGIN LAYER {i+1}")
			idxs, x, y, msg, cs = self.compute_layer(i)
			if len(idxs) > 0:
				mock_messenger.broadcast("MUL", i, msg)
				resps = mock_messenger.collect(i)
				resps.append(msg)
				self.finish_layer(idxs, x, y, resps, cs)
		return self.get_outputs()

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

class Circuit:

	def __init__(self, path, input_types):
		with open(path, "r") as f:
			data = f.read()
		circuit, n_layers, outputs = self.load_bristol_circuit(data, input_types)
		self.output_indexes = outputs
		self.circuit_layers = [[] for _ in range(n_layers+1)]
		lines = [k for k in data.split("\n")[4:] if 'EQW' not in k]
		order = [int(i.split()[-2])+2 for i in lines]
		self.tape_len = max(order)+1
		for i in order:
			gate = circuit[i]
			if gate[1] != None:
				self.circuit_layers[gate[0][1]].append((i, gate[0][2], gate[1]))

	def load_bristol_circuit(self, data, input_types):
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
