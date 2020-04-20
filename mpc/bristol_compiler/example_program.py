from compiler import MPCProgram

mpc = MPCProgram()
x = mpc.input(64)
y = mpc.input(64)
addition = mpc.add64(x, y)
subtraction = mpc.sub64(x, y)
mpc.output(addition, subtraction)
mpc.compile("example.txt")
