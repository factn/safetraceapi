from shamir import Shamir, TripleShare, randelement

def gen_triples(t, n, n_triples):
	triples = [[] for _ in range(n)]
	for i in range(n_triples):
		a = randelement()
		b = randelement()
		c = a*b
		a_shares = Shamir(t, n).share_secret(a)
		b_shares = Shamir(t, n).share_secret(b)
		c_shares = Shamir(t, n).share_secret(c)
		for i in range(n):
			triples[i].append(TripleShare(a_shares[i], b_shares[i], c_shares[i]))
	return triples

class TripleGeneration:

	def __init__(self, index, shamir, messenger, batch_size=1000, n_batches=1):
		assert shamir.t*2 < shamir.n, "triple generation requires t>n/2"
		self.index = index
		self.shamir = shamir
		self.messenger = messenger
		self.batch_size = batch_size
		self.n_batches = n_batches
		self.triples = []

	def run(self):
		for k in range(self.n_batches):
			round_ = 2*k
			msgs = self.shamir.generate_triples_round_1(self.batch_size)
			for i in range(len(msgs)):
				if i+1 != self.index:
					self.messenger.send(i+1, "TRIP-AB", round_, msgs[i])
			resps = self.messenger.collect(round_, full_quorum=True)
			resps.append(msgs[self.index-1])

			round_+=1
			a_shares, b_shares, msgs = self.shamir.generate_triples_round_2(resps)
			for i in range(len(msgs)):
				if i+1 != self.index:
					self.messenger.send(i+1, "TRIP-C", round_, msgs[i])
			resps = self.messenger.collect(round_, full_quorum=True)
			resps.append(msgs[self.index-1])

			self.triples.extend(self.shamir.generate_triples_round_3(a_shares, b_shares, resps))
