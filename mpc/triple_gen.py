class TripleGeneration:

	def __init__(self, index, shamir, messenger, batch_size=1000, n_batches=10):
		self.index = index
		self.shamir = shamir
		self.messenger = messenger
		self.batch_size = batch_size
		self.n_batches = n_batches
		self.triples = []

	def run():
		for _ in n_batches:
			round_ = 0
			msgs_1 = self.shamir.generate_triples_round_1(batch_size)
			for i in range(len(msgs_1)):
				if i+1 != index:
					self.messenger.send(i+1, round_, msgs_1[i])
			resps_1 = self.messenger.collect(round_, full_quorum=True)
			resps_1.append(msgs[index-1])

			round_+=1
			msgs_2 = self.shamir.generate_triples_round_2(resps_1)
			for i in range(len(msgs_2)):
				if i+1 != index:
					self.messenger.send(i+1, round_, msgs_2[i])
			resps_2 = self.messenger.collect(round_, full_quorum=True)
			resps_2.append(msgs_2[index-1])

			self.triples.append(self.shamir.generate_triples_round_3(resps_2))