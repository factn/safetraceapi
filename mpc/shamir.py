from secrets import randbelow
from gf256 import GF256

class Shamir:
	'''Shamir Secret Sharing over the field GF(2^8)
	for a given threshold (t) and number of parties (n)
	'''

	def __init__(self, threshold, n_parties):
		assert threshold < n_parties, "cannot require more shares for reconstruction than number of parties"
		self.t = threshold
		self.n = n_parties

	def share_secret(self, secret):
		'''Takes a GF256 element (or int [0,255]) and splits it into n Shamir Secret Shares 
		where >t secret shares are required to reconstruct the shared value
		'''

		if type(secret) != GF256:
			secret = GF256(secret)
		coefficients = [secret] + [randelement() for _ in range(self.t)]
		return [Share(i+1, evaluate_polynomial(coefficients, GF256(i+1))) for i in range(self.n)]

	def reconstruct_secret(self, shares):
		'''Takes a set of >t shares and interpolates the unique polynomial 
		passing through them to recover the secret value at f(0). 
		'''

		assert len(shares) > self.t, "not enough shares for interpolation"
		secret = GF256(0)
		for i in range(len(shares)):
			x = GF256(shares[i].x)
			num = shares[i].y
			denom = GF256(1)
			for k in range(len(shares)):
				if k != i:
					num = num * (GF256(0) - GF256(shares[k].x))
					denom = denom * (x - GF256(shares[k].x))
			secret += num/denom
		return secret

	def share_bitstring_secret(self, bits):
		'''Takes an arbitrary string of bits and splits the data among n parties.
		Each party receives an ordered list of l Shamir Secret Shares where l = length of bitstring. 
		'''

		output = [[] for _ in range(self.n)]
		for b in bits:
			s = GF256(0)
			if b=='1':
				s = GF256(1)
			elif b=='0':
				pass
			else:
				raise ValueError("not a valid bitstring")
			shares = self.share_secret(s)
			for i in range(self.n):
				output[i].append(shares[i])
		return output

	def reconstruct_bitstring_secret(self, all_shares):
		'''Takes >t ordered lists of shares and reconstructs the underlying secret bitstring
		'''

		assert len(all_shares) > self.t, "not enough shares for reconstruction"
		n_shares = len(all_shares[0])
		bitstring = ''
		for i in range(n_shares):
			shares = [s[i] for s in all_shares]
			val = self.reconstruct_secret(shares)
			if int(val) == 0:
				bitstring = bitstring+'0'
			elif int(val) == 1:
				bitstring = bitstring+'1'
			else:
				raise ValueError("Reconstructed a value outside [0,1]")
		return bitstring

	def mul_gates_round_1(self, x_shares, y_shares, triples):
		''' First phase (before communication) of secure share multiplication protocol for MPC.
		'''

		return [self.multiply_shares_round_1(x_shares[i], y_shares[i], triples[i]) for i in range(len(triples))]

	def mul_gates_round_2(self, x_shares, y_shares, er_lists, cs):
		''' Second phase (after communication) of secure share multiplication protocol for MPC.
		'''

		assert len(er_lists) > self.t, "not enough shares for reconstruction"
		return [self.multiply_shares_round_2(x_shares[i], y_shares[i], [e[i][0] for e in er_lists], [r[i][1] for r in er_lists], cs[i]) for i in range(len(x_shares))]

	def generate_triples_round_1(self, n_triples):
		'''First round of secure triple generation protocol for MPC (offline phase)
		'''

		assert 2*self.t < self.n, "triple generation requires t>n/2"
		a_shares = [self.share_secret(randelement()) for _ in range(n_triples)]
		b_shares = [self.share_secret(randelement()) for _ in range(n_triples)]
		output = []
		for i in range(self.n):
			player_as = [a[i] for a in a_shares]
			player_bs = [b[i] for b in b_shares]
			output.append([(player_as[j], player_bs[j]) for j in range(len(player_as))])
		return output

	def generate_triples_round_2(self, ab_lists):
		'''Second round of secure triple generation protocol for MPC (offline phase)
		'''

		assert 2*self.t < self.n, "triple generation requires t>n/2"
		assert len(ab_lists) == self.n, f"triple generation requires all {self.n} participants"
		a_shares = []
		b_shares = []
		player_c_shares = [[] for _ in range(self.n)]
		for i in range(len(ab_lists[0])):
			a_share_shares = [j[i][0] for j in ab_lists]
			b_share_shares = [j[i][1] for j in ab_lists]
			a_share = a_share_shares[0]+a_share_shares[1]
			b_share = b_share_shares[0]+b_share_shares[1]
			for j in range(2,len(a_share_shares)):
				a_share += a_share_shares[j]
				b_share += b_share_shares[j]
			schurr = a_share.y*b_share.y
			v = schurr*get_lagrange_coefficients(self.n)[a_share.x-1]
			a_shares.append(a_share)
			b_shares.append(b_share)
			c_shares = self.share_secret(v)
			for j in range(len(c_shares)):
				player_c_shares[j].append(c_shares[j])
		return a_shares, b_shares, player_c_shares

	def generate_triples_round_3(self, a_shares, b_shares, c_share_shares):
		'''Final round of secure triple generation protocol for MPC (offline phase)
		'''

		assert 2*self.t < self.n, "triple generation requires t>n/2"
		assert len(c_share_shares) == self.n, f"triple generation requires all {self.n} participants"
		triples = []
		for i in range(len(c_share_shares[0])):
			c_shares = [j[i] for j in c_share_shares]
			c_share = c_shares[0]+c_shares[1]
			for j in range(2,len(c_shares)):
				c_share += c_shares[j]
			triples.append(TripleShare(a_shares[i], b_shares[i], c_share))
		return triples

	def multiply_shares_round_1(self, s1, s2, triple):
		return (s1 - triple.a, s2 - triple.b)

	def multiply_shares_round_2(self, s1, s2, ep_shares, rho_shares, c):
		epsilon = self.reconstruct_secret(ep_shares)
		rho = self.reconstruct_secret(rho_shares)
		v1 = s2.scalar_mul(epsilon)
		v2 = s1.scalar_mul(rho)
		v3 = v1+v2+c
		er = epsilon*rho
		return v3.scalar_shift(GF256(0)-er)

class Share:
	'''A Shamir Secret Share
	'''

	def __init__(self, x, y):
		assert x < 256, "player index too large"
		if type(y) != GF256:
			y = GF256(y)
		self.x = x
		self.y = y

	def __add__(self, other):
		assert self.x == other.x, "mismatching player index"
		return Share(self.x, self.y+other.y)

	def __sub__(self, other):
		assert self.x == other.x, "mismatching player index"
		return Share(self.x, self.y-other.y)

	def scalar_shift(self, scalar):
		if type(scalar) != GF256:
			scalar = GF256(scalar)
		return Share(self.x, self.y+scalar)

	def scalar_mul(self, scalar):
		if type(scalar) != GF256:
			scalar = GF256(scalar)
		return Share(self.x, self.y*scalar)

	def __str__(self):
		return f"({self.x}, {int(self.y)})"

	def __repr__(self):
		return f"({self.x}, {int(self.y)})"

class TripleShare:
	'''Shamir Secret Shares of three values a, b and c where a*b = c.
	'''

	def __init__(self, a, b, c):
		assert a.x == b.x == c.x, f"Mismatching x values for a, b and c share: {(a.x, b.x, c.x)}"
		self.a = a
		self.b = b
		self.c = c

##
## Helper Math
##

def evaluate_polynomial(coefficients, x_value):
	result = coefficients[-1]
	for i in range(2, len(coefficients)+1):
		result = result*x_value
		result = result + coefficients[-i]
	return result

def get_lagrange_coefficients(n):
	xs = [GF256(i+1) for i in range(n)]
	coeffs = []
	for i in range(n):
		x = xs[i]
		num = GF256(1)
		denom = GF256(1)
		for k in range(n):
			if k != i:
				num = num * (GF256(0) - xs[k])
				denom = denom * (x - xs[k])
		coeffs.append(num/denom)
	return coeffs

def randelement():
	return GF256(__randrange(0, 255))

def __randrange(lower, upper):
	return randbelow(upper-lower)+lower
