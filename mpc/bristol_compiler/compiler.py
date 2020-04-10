import os

class MPCProgram:

    def __init__(self, circuit_dir=None):
        self.tape_len = 0
        self.input_len = 0
        self.output_len = 0
        self.lines = []
        self.output_indexes = []
        if circuit_dir == None:
            self.circuit_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bristol_circuits")
        else:
            self.circuit_dir = circuit_dir

    def compile(self, name):
        self.__collect_outputs()
        prefix = f"{self.tape_len-self.input_len} {self.tape_len}\n1 {self.input_len}\n1 {self.output_len}\n\n"
        text = prefix+''.join(self.lines)
        text = text[:-1]
        with open(os.path.join(self.circuit_dir, name), "w") as f:
            f.write(text)

    def input(self, length):
        self.tape_len += length
        self.input_len += length
        return list(range(self.tape_len-length, self.tape_len))

    def output(self, *index_lists):
        length = 0
        indexes = []
        for i in index_lists:
            length += len(i)
            indexes.extend(i)
        self.output_len += length
        self.output_indexes = indexes

    def add64(self, b1, b2):
        assert len(b1) == 64, f"invalid input length {len(b1)}"
        assert len(b2) == 64, f"invalid input length {len(b2)}"
        return self.shift_circuit("add64.txt", b1+b2, 64)

    def sub64(self, b1, b2):
        assert len(b1) == 64, f"invalid input length {len(b1)}"
        assert len(b2) == 64, f"invalid input length {len(b2)}"
        return self.shift_circuit("sub64.txt", b1+b2, 64)

    def lessthan32(self, b1, b2):
        assert len(b1) == 32, f"invalid input length {len(b1)}"
        assert len(b2) == 32, f"invalid input length {len(b2)}"
        return self.shift_circuit("lessthan32.txt", b1+b2, 1)

    def mul64mod(self, b1, b2):
        assert len(b1) == 64, f"invalid input length {len(b1)}"
        assert len(b2) == 64, f"invalid input length {len(b2)}"
        return self.shift_circuit("mul64mod.txt", b1+b2, 64)  

    def eqzero64(self, b):
        assert len(b) == 64, f"invalid input length {len(b)}"
        return self.shift_circuit("eqzero64.txt", b, 1)     

    def xor(self, b1, b2):
        assert len(b1) == 1, f"invalid input length {len(b1)}"
        assert len(b2) == 1, f"invalid input length {len(b2)}"
        n = self.tape_len
        self.lines.append(f"2 1 {b1[0]} {b2[0]} {n} XOR\n")
        self.tape_len += 1
        return [n]

    def and_(self, b1, b2):
        assert len(b1) == 1, f"invalid input length {len(b1)}"
        assert len(b2) == 1, f"invalid input length {len(b2)}"
        n = self.tape_len
        self.lines.append(f"2 1 {b1[0]} {b2[0]} {n} AND\n")
        self.tape_len += 1
        return [n]

    def not_(self, b):
        assert len(b) == 1, f"invalid input length {len(b1)}"
        n = self.tape_len
        self.lines.append(f"1 1 {b} {n} INV\n")
        self.tape_len += 1
        return [n]

    def shift_circuit(self, circuit_name, input_indexes, output_len):
        file = os.path.join(self.circuit_dir, circuit_name)
        with open(file, "r") as f:
            raw_text = f.read()
        circuit = [i.split() for i in raw_text.split("\n")]
        n_ops = int(circuit[0][0])
        substitute_dict={}
        n_inputs = len(input_indexes)
        for i in range(n_inputs):
            substitute_dict[i] = input_indexes[i]
        for gate in circuit[3:]:
            if gate == []:
                continue
            elif gate[-1] == "XOR" or gate[-1] == "AND":
                nums = [int(gate[-4]), int(gate[-3]), int(gate[-2])]
                for i in range(len(nums)):
                    if nums[i] in range(n_inputs):
                        nums[i] = substitute_dict[nums[i]]
                    else:
                        nums[i] = nums[i]-n_inputs+self.tape_len
                self.lines.append(f"2 1 {nums[0]} {nums[1]} {nums[2]} {gate[-1]}\n")
            elif gate[-1]=="INV":
                nums = [int(gate[-3]), int(gate[-2])]
                for i in range(len(nums)):
                    if nums[i] in range(n_inputs):
                        nums[i] = substitute_dict[nums[i]]
                    else:
                        nums[i] = nums[i]-n_inputs+self.tape_len
                self.lines.append(f"1 1 {nums[0]} {nums[1]} INV\n")
            else:
                raise ValueError(f"Could not interpret bristol circuit line: {gate}")
        self.tape_len += n_ops
        return list(range(self.tape_len-output_len, self.tape_len))

    def __collect_outputs(self):
        if len(self.output_indexes) == 0 or self.output_len == 0:
            raise ValueError("Must set outputs before compiling!")
        current_outputs = self.output_indexes
        if current_outputs != list(range(self.tape_len-self.output_len, self.tape_len)):
            outputs = list(range(self.tape_len-self.output_len, self.tape_len))
            for i in range(len(self.lines)):
                new_words = []
                for word in self.lines[i].split():
                    try:
                        if int(word) in current_outputs:
                            idx = current_outputs.index(int(word))
                            new_words.append(f'{outputs[idx]}')
                        elif int(word) in outputs:
                            idx = outputs.index(int(word))
                            new_words.append(f'{current_outputs[idx]}')
                        else:
                            new_words.append(word)
                    except:
                        new_words.append(word)
                self.lines[i] = ' '.join(new_words)+'\n'
