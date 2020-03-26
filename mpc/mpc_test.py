from circuit import Circuit
from shamir import Shamir, gen_triples
from messenger import MockMessenger
from multiprocessing import Queue, Process
import time
from threading import Thread

def consumer(mq, n, result, t, processes):
    vals = []
    while len(vals) < n:
        if not mq.empty():
            vals.append(mq.get())
    reconstructed = Shamir(t, n).reconstruct_bitstring_secret(vals)
    assert eval('0b'+reconstructed) == result, "result incorrect"
    mq.close()
    for p in processes:
        p.terminate()

def run_circuit_process(t, n, c_path, index, queues, main_queue, inputs, triples):
    shamir = Shamir(t, n)
    messenger = MockMessenger(t, n, index, queues)
    c = Circuit(c_path, ['S' for _ in range(len(inputs))])
    outputs = c.evaluate(inputs, shamir=shamir, messenger=messenger, triples=triples)
    main_queue.put(outputs)

def test_mpc(t, n, c_path, n_triples, inputs, result):
    triples = gen_triples(t, n, n_triples)
    mq = Queue()
    queues = [Queue() for _ in range(n)]
    share_inputs = [Shamir(t, n).share_bitstring_secret(i) for i in inputs]
    processes = []
    for i in range(n):
        inputs = []
        for si in share_inputs:
            inputs.extend(si[i])
        p = Process(target=run_circuit_process, args=(t, n, c_path, i+1, queues, mq, inputs, triples[i]))
        processes.append(p)
    start = time.time()
    for p in processes:
        p.start()
    t1 = Thread(target=consumer, args=(mq, n, result, t, processes))
    t1.start()
    for p in processes:
        if p.is_alive():
            p.join()
    t1.join(n)
    print(f"time: {round(time.time()-start, 4)} seconds")
    for q in queues:
        q.close()
        q.join_thread()
    mq.join_thread()

def test_mul32_circuit():
    t = 2
    n = 5
    c_path = "circuits/mul32_circuit.txt"
    n_triples = 6000
    x = 101
    y = 50000
    result = x*y
    x_bin = bin(x)[2:]
    while len(x_bin) < 32:
        x_bin = '0'+x_bin
    y_bin = bin(y)[2:]
    while len(y_bin) < 32:
        y_bin = '0'+y_bin
    test_mpc(t, n, c_path, n_triples, [x_bin, y_bin], result)

def test_tiny_circuit():
    t = 2
    n = 5
    c_path = "circuits/tiny_circuit.txt"
    n_triples = 2
    x = '01'
    y = '10'
    result = 3
    test_mpc(t, n, c_path, n_triples, [x,y], result)

if __name__ == "__main__":
    print("--BEGIN SHORT TEST (4 gates)--")
    test_tiny_circuit()
    print("--BEGIN LONG TEST (12374 gates)--")
    test_mul32_circuit()
