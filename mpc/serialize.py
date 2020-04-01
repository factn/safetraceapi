from shamir import Share, TripleShare

def serialize_shares(shares):
	return [[int(s.x), int(s.y)] for s in shares]

def deserialize_shares(flat_shares):
	return [Share(s[0], s[1]) for s in flat_shares]

def serialize_triples(triples):
	return [[int(t.a.x), int(t.a.y), int(t.b.y), int(t.c.y)] for t in triples]

def deserialize_triples(flat_triples):
	return [TripleShare(Share(t[0], t[1]), Share(t[0], t[2]), Share(t[0], t[3])) for t in flat_triples]

def serialize_mul_msg(er_list):
	return [[int(s1.x), int(s1.y), int(s2.x), int(s2.y)] for s1, s2 in er_list]

def deserialize_mul_msg(flat_list):
	return [(Share(s[0], s[1]), Share(s[2], s[3])) for s in flat_list]

def serialize_triple_ab_msg(playerABs):
	playerAs = [[int(a.x), int(a.y)] for a in playerABs[0]]
	playerBs = [[int(b.x), int(b.y)] for b in playerABs[1]]
	return [playerAs, playerBs]

def deserialize_triple_ab_msg(flatABs):
	playerAs = [Share(a[0], a[1]) for a in flatABs[0]]
	playerBs = [Share(b[0], b[1]) for b in flatABs[1]]
	return (playerAs, playerBs)

def serialize_triple_c_msg(c_shares):
	return serialize_shares(c_shares)

def deserialize_triple_c_msg(flat_shares):
	return deserialize_shares(flat_shares)