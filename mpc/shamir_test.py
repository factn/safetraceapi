from shamir import Shamir, randelement

def test_reconstruction():
	t = 2
	n = 2*t+1
	shamir = Shamir(t, n)
	secret = randelement()
	shares = shamir.share_secret(secret)
	reconstructed = shamir.reconstruct_secret(shares[:t+1])
	assert secret == reconstructed, "reconstructed the wrong value"

def test_secure_addition():
	t = 2
	n = 2*t+1
	shamir = Shamir(t, n)
	s1 = randelement()
	s2 = randelement()
	answer = s1+s2
	shares1 = shamir.share_secret(s1)
	shares2 = shamir.share_secret(s2)
	# Each party locally adds their share of secret 1 and 2
	final_shares = [shares1[i]+shares2[i] for i in range(n)]
	# Check
	reconstructed = shamir.reconstruct_secret(final_shares[0:t+1])
	assert answer == reconstructed, "reconstructed the wrong value"

def test_secure_multiplication():
	t = 2
	n = 2*t+1
	n_muls = 5
	shamir = Shamir(t, n)
	xs = [randelement() for _ in range(n_muls)]
	ys = [randelement() for _ in range(n_muls)]
	answers = [xs[i]*ys[i] for i in range(n_muls)]
	x_sharings = [shamir.share_secret(xs[i]) for i in range(n_muls)]
	y_sharings = [shamir.share_secret(ys[i]) for i in range(n_muls)]
	triples = test_triple_creation(t, n, n_muls)

	##
	## ROUND 1
	##

	broadcasts = []
	# Each party
	for i in range(n):
		# computes intermediate values (er_list) for shares to be multiplied
		er_list = shamir.mul_gates_round_1([x[i] for x in x_sharings], [y[i] for y in y_sharings], triples[i])
		# broadcasts the intermediate values to all other parties
		broadcasts.append(er_list)
	
	##
	## ROUND 2
	##

	player_result_shares = []
	# Each party
	for i in range(n):
		# Collects broadcasted messages and uses these intermediate values to compute result shares
		result_shares = shamir.mul_gates_round_2([x[i] for x in x_sharings], [y[i] for y in y_sharings], broadcasts, [t.c for t in triples[i]])
		player_result_shares.append(result_shares)

	# Check values
	for i in range(len(answers)):
		reconstructed = shamir.reconstruct_secret([p[i] for p in player_result_shares])
		assert reconstructed == answers[i], "reconstructed the wrong value"


def test_triple_creation(t, n, n_triples):
	shamir = Shamir(t, n)

	##
	## ROUND 1
	##

	player_ab_lists = [[] for _ in range(n)]
	# Each party
	for _ in range(n):
		# computes random shared values
		ab_lists = shamir.generate_triples_round_1(n_triples)
		# sends each other party their particular shares (point to point)
		for i in range(n):
			player_ab_lists[i].append(ab_lists[i])

	##
	## ROUND 2
	##

	player_a_shares = []
	player_b_shares = []
	player_c_share_shares = [[] for _ in range(n)]
	# Each party
	for i in range(n):
		# collects received ab_list messages and computes intermediate values
		a_shares, b_shares, c_share_shares = shamir.generate_triples_round_2(player_ab_lists[i])
		player_a_shares.append(a_shares)
		player_b_shares.append(b_shares)
		# sends each party their c_share_shares (point to point)
		for j in range(n):
			player_c_share_shares[j].append(c_share_shares[j])

	##
	## ROUND 3
	##

	player_triples = []
	# Each party
	for i in range(n):
		# collects received c_share_share messages and computes the result TripleShare values.
		triples = shamir.generate_triples_round_3(player_a_shares[i], player_b_shares[i], player_c_share_shares[i])
		player_triples.append(triples)

	## Check
	for i in range(len(player_triples[0])):
		check_a = shamir.reconstruct_secret([p[i].a for p in player_triples])
		check_b = shamir.reconstruct_secret([p[i].b for p in player_triples])
		check_c = shamir.reconstruct_secret([p[i].c for p in player_triples])
		assert check_a*check_b == check_c, "invalid triple was created"
	return player_triples


if __name__ == "__main__":
	test_reconstruction()
	test_secure_addition()
	test_secure_multiplication()
	test_triple_creation(1, 3, 500)
	print("PASS")
