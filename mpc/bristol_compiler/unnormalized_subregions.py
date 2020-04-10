from compiler import MPCProgram

def compile_unnormalized_subregion(num_users, num_regions):
	mpc = MPCProgram()
	zero64 = mpc.input(64)
	in_region = []
	infection_status = []
	for _ in range(num_users):
		infection_status.append([mpc.input(1), mpc.input(1)])
		user_in_region = [mpc.input(1) for _ in range(num_regions)]
		in_region.append(user_in_region)
	scores = []
	for i in range(num_regions):
		score = zero64
		for j in range(num_users):
			inside = in_region[j][i]
			statusLS, statusMS = infection_status[j]
			b1 = mpc.and_(statusLS, inside)
			b2 = mpc.and_(statusMS, inside)
			num = b1+b2+zero64[:62]
			score = mpc.add64(score, num)
		scores.append(score)
	mpc.output(*scores)
	mpc.compile(f"unnormalized_subregion_{num_users}_{num_regions}.txt")

if __name__ == '__main__':
	import sys
	args = sys.argv[1:]
	compile_unnormalized_subregion(int(args[0]), int(args[1]))

