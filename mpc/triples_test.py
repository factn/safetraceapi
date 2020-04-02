from shamir import Shamir
from messenger import Messenger
from triples import TripleGeneration
from multiprocessing import Queue, Process
import time

def consumer(mq, t, n, processes):
    vals = []
    while len(vals) < n:
        if not mq.empty():
            vals.append(mq.get())
    n_triples = len(vals[0])
    for i in [0, 1, n_triples-2, n_triples-1]:
    	trips = [vals[j][i] for j in range(n)]
    	a_shares = [t.a for t in trips]
    	b_shares = [t.b for t in trips]
    	c_shares = [t.c for t in trips]
    	a = Shamir(t, n).reconstruct_secret(a_shares)
    	b = Shamir(t, n).reconstruct_secret(b_shares)
    	c = Shamir(t, n).reconstruct_secret(c_shares)
    	assert a*b==c, "triples are not equal"

def run_triplegen_process(t, n, index, queues, main_queue, batch_size, n_batches):
    shamir = Shamir(t, n)
    messenger = Messenger(t, n, index, queues, "")
    tg = TripleGeneration(index, shamir, messenger, batch_size=batch_size, n_batches=n_batches)
    tg.run()
    main_queue.put(tg.triples)

def test_triple_generation(t, n, batch_size, n_batches):
    mq = Queue()
    queues = [Queue() for _ in range(n)]
    processes = []
    for i in range(n):
        p = Process(target=run_triplegen_process, args=(t, n, i+1, queues, mq, batch_size, n_batches))
        processes.append(p)
    start = time.time()
    for p in processes:
        p.start()
    t1 = Process(target=consumer, args=(mq, t, n, processes))
    t1.start()
    for p in processes:
        if p.is_alive():
            p.join()
    t1.join()
    print(f"time: {round(time.time()-start, 4)} seconds")
    for q in queues:
        q.close()
        q.join_thread()
    mq.close()
    mq.join_thread()

if __name__ == "__main__":
	print("--Batch Size: 1000, Batches: 1--")
	test_triple_generation(2, 5, 1000, 1)
	print("--Batch Size: 100, Batches: 10--")
	test_triple_generation(2, 5, 100, 10)
	print("--Batch Size: 1000, Batches: 5--")
	test_triple_generation(2, 5, 1000, 5)
