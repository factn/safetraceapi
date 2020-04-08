from lexer import getTokens
import os

TYPES = {
    "BIT128": {
        "length": 128
    },
    "BIT64": {
        "length": 64
    },
    "BIT32": {
        "length": 32
    },  
    "BIT": {
        "length": 1
    },
}

class Compiler:

    def __init__(self, circuit_dir=None):
        self.tape_len = 0
        self.input_len = 0
        self.id2var = {}
        self.text = ""
        if circuit_dir == None:
            self.circuit_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bristol_circuits")
        else:
            self.circuit_dir = circuit_dir
        self.input_vars = []
        self.output_vars = []

    def compile(self, script_name, circuit_name):
        self.text=self.build("scripts/"+script_name)
        with open(os.path.join(self.circuit_dir, circuit_name), "w") as f:
            f.write(self.text)

    def build(self, filename):
        self.reset()
        toks = getTokens(filename)
        lines = [[t for t in toks if t[2] == i] for i in range(1, toks[-1][2] + 1)]
        for line in lines:
            if len(line) > 0:
                if line[0][0] == "INPUT":
                    if not self.input(line[1][0], line[2]):
                        return f"INPUT ERROR LINE {line[0][2]}"

                #assignment
                if line[0][0] == "ASSIGN":
                    if not self.assign(line[1][0], line[2], line[4:]):
                        return f"ASSIGNEMNT ERROR LINE {line[0][2]} {repr(line)}"

                if line[0][0] == "OUTPUT":
                    if not self.output(line[1][0], line[2]):
                        return f"OUTPUT ERROR LINE {line[0][2]}"
        prefix = f"{self.tape_len-self.input_len} {self.tape_len}\n{len(self.input_vars)}"
        for v in self.input_vars:
            prefix += f' {TYPES[self.id2var[v]["type"]]["length"]}'
        prefix += f"\n{len(self.output_vars)}"
        for v in self.output_vars:
            prefix += f' {TYPES[self.id2var[v]["type"]]["length"]}'
        prefix += "\n\n"
        self.text = prefix+self.text
        return self.text

    def input(self, type_, name):
        if type_ not in TYPES.keys():
            return False
        if name[0] != "ID":
            return False
        self.id2var[name[1]] = {"type": type_, "addresses": list(range(self.tape_len, self.tape_len+TYPES[type_]["length"]))}
        self.tape_len += TYPES[type_]["length"]
        self.input_len += TYPES[type_]["length"]
        self.input_vars.append(name[1])
        return True

    def assign(self, type_, name, expr):
        if type_ not in TYPES.keys():
            return False
        if name[0] != "ID":
            return False

        # assign the output of a function
        if self.functions(expr[0][0], expr[1:]):
            self.id2var[name[1]] = {
                "addresses": list(range(self.tape_len - TYPES[type_]["length"], self.tape_len)),
                "type": type_,
            }
            return True

        # assign a slice of a previous variable
        elif expr[0][1] in self.id2var.keys() and expr[1][0] == "LBRACK":
            vals = expr[2][1], expr[4][1]
            if vals[1] - vals[0] != TYPES[type_]["length"]:
                return False
            else:
                self.id2var[name[1]] = {
                    "addresses": self.id2var[expr[0][1]]["addresses"][vals[0]:vals[1]],
                    "type": type_
                }
                return True

        # assign a concatenation of two previous variables
        elif expr[0][1] in self.id2var.keys() and expr[1][0] == "COLON" and expr[2][1] in self.id2var.keys():
            if TYPES[type_]["length"] != TYPES[self.id2var[expr[0][1]]["type"]]["length"] + TYPES[self.id2var[expr[2][1]]["type"]]["length"]:
                return False
            else:
                self.id2var[name[1]] = {
                    "addresses": self.id2var[expr[0][1]]["addresses"] + self.id2var[expr[2][1]]["addresses"],
                    "type": type_
                }
                return True
        return False

    def output(self, type_, name):
        if type_ not in TYPES.keys():
            return False
        if name[0] != "ID":
            return False
        if name[1] not in self.id2var.keys():
            return False
        self.output_vars.append(name[1])
        return True

    def functions(self, name, expr):
        if name=="XOR" or name=="AND":
            if expr[0][0] == "LPAREN" and expr[4][0] == "RPAREN":
                ids = [expr[1][1], expr[3][1]]
                addrs = []
                if self.id2var[ids[0]]["type"] == "BIT":
                    addrs.append(self.id2var[ids[0]]["addresses"][0])
                    if self.id2var[ids[1]]["type"] == "BIT":
                        addrs.append(self.id2var[ids[1]]["addresses"][0])
                    else:
                        return False
                    self.text += f"2 1 {addrs[0]} {addrs[1]} {self.tape_len} {name}\n"
                    self.tape_len += 1
                    return True

        if name=="NOT":
            if expr[0][0] == "LPAREN" and expr[2][0] == "RPAREN":
                id_ = expr[1][1]
                for i in self.id2var[id_]["addresses"]:
                    self.text += f"1 1 {i} {self.tape_len} INV\n"
                    self.tape_len += 1
                return True

        if name=="LT32":
            if expr[0][0] == "LPAREN" and expr[4][0] == "RPAREN":
                ids = [expr[1][1], expr[3][1]]
                indexes = []
                for i in range(len(ids)):
                    if self.id2var[ids[i]]["type"] == "BIT32":
                        indexes.extend(self.id2var[ids[i]]["addresses"])
                    else:
                        return False
                file = os.path.join(self.circuit_dir, "lessthan32.txt")
                with open(file, "r") as f:
                    raw_text = f.read()
                circuit = [i.split() for i in raw_text.split("\n")]
                n_ops = int(circuit[0][0])
                self.shift_circuit(circuit[1:], indexes, n_ops)
                return True

        if name=="ADD64" or name=="SUB64" or name=="MUL64MOD":
            if expr[0][0] == "LPAREN" and expr[4][0] == "RPAREN":
                ids = [expr[1][1], expr[3][1]]
                indexes = []
                for i in range(len(ids)):
                    if self.id2var[ids[i]]["type"] == "BIT64":
                        indexes.extend(self.id2var[ids[i]]["addresses"])
                    else:
                        return False
                file = None
                if name == "ADD64":
                    file = os.path.join(self.circuit_dir, "add64.txt")
                elif name == "SUB64":
                    file = os.path.join(self.circuit_dir, "sub64.txt")
                elif name == "MUL64MOD":
                    file = os.path.join(self.circuit_dir, "mul64mod.txt")
                with open(file, "r") as f:
                    raw_text = f.read()
                circuit = [i.split() for i in raw_text.split("\n")]
                n_ops = int(circuit[0][0])
                self.shift_circuit(circuit[1:], indexes, n_ops)
                return True

        if name=="EQZ64":
            if expr[0][0] == "LPAREN" and expr[2][0] == "RPAREN":
                id_ = expr[1][1]
                if self.id2var[id_]["type"] == "BIT64":
                    indexes = self.id2var[id_]["addresses"]
                else:
                    return False
                file = os.path.join(self.circuit_dir, "eqzero64.txt")
                with open(file, "r") as f:
                    raw_text = f.read()
                circuit = [i.split() for i in raw_text.split("\n")]
                n_ops = int(circuit[0][0])
                self.shift_circuit(circuit[1:], indexes, n_ops)
                return True
        return False

    def shift_circuit(self, circuit, input_indexes, circuit_length):
        substitute_dict={}
        n_inputs = len(input_indexes)
        for i in range(n_inputs):
            substitute_dict[i] = input_indexes[i]
        for gate in circuit:
            if gate == []:
                continue
            if gate[-1] == "XOR" or gate[-1] == "AND":
                nums = [int(gate[-4]), int(gate[-3]), int(gate[-2])]
                for i in range(len(nums)):
                    if nums[i] in range(n_inputs):
                        nums[i] = substitute_dict[nums[i]]
                    else:
                        nums[i] = nums[i]-n_inputs+self.tape_len
                self.text += f"2 1 {nums[0]} {nums[1]} {nums[2]} {gate[-1]}\n"
            if gate[-1]=="INV":
                nums = [int(gate[-3]), int(gate[-2])]
                for i in range(len(nums)):
                    if nums[i] in range(n_inputs):
                        nums[i] = substitute_dict[nums[i]]
                    else:
                        nums[i] = nums[i]-n_inputs+self.tape_len
                self.text += f"1 1 {nums[0]} {nums[1]} INV\n"            
        self.tape_len += circuit_length


    def reset(self):
        self.tape_len = 0
        self.input_len = 0
        self.id2var = {}
        self.text = ""
        self.input_vars = []
        self.output_vars = []
