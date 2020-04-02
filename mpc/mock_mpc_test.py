from circuit import Circuit
from shamir import Shamir
from triples import gen_triples
from messenger import Messenger
from multiprocessing import Queue, Process
import time

def consumer(mq, n, result, t, processes, reflect):
    vals = []
    while len(vals) < n:
        if not mq.empty():
            vals.append(mq.get())
    reconstructed = Shamir(t, n).reconstruct_bitstring_secret(vals)[::-1]
    if reflect:
        reconstructed = reconstructed[int(len(reconstructed)/2):]+reconstructed[:int(len(reconstructed)/2)]
    assert eval('0b'+reconstructed) == eval('0b'+result), "result incorrect"

def run_circuit_process(t, n, c_path, index, queues, main_queue, inputs, triples):
    shamir = Shamir(t, n)
    messenger = Messenger(t, n, index, queues, "--UNIQUE COMPUTATION ID--")
    c = Circuit(c_path, ['S' for _ in range(len(inputs))])
    outputs = c.evaluate(inputs, shamir=shamir, messenger=messenger, triples=triples)
    main_queue.put(outputs)

def test_mpc(t, n, c_path, n_triples, inputs, result, reflect=False):
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
    t1 = Process(target=consumer, args=(mq, n, result, t, processes, reflect))
    t1.start()
    for p in processes:
        p.join()
    t1.join()
    print(f"time: {round(time.time()-start, 4)} seconds")
    while not mq.empty():
        mq.get()
    mq.close()
    for q in queues:
        q.close()
        q.join_thread()
    mq.join_thread()

def test_add64_circuit():
    t = 2
    n = 5
    c_path = "bristol_circuits/add64.txt"
    n_triples = 500
    for x,y in [(100, 200), (2**30, 2**10), (2**64-1, 2**64-1)]:
        result = bin((x+y)%(2**64))[2:]
        x_bin = bin(x)[2:]
        while len(x_bin) < 64:
            x_bin = '0'+x_bin
        y_bin = bin(y)[2:]
        while len(y_bin) < 64:
            y_bin = '0'+y_bin
        test_mpc(t, n, c_path, n_triples, [x_bin[::-1], y_bin[::-1]], result)

def test_sub64_circuit():
    t = 2
    n = 5
    c_path = "bristol_circuits/sub64.txt"
    n_triples = 500
    for x,y in [(1000, 2010), (2025, 111), (2**64-2, 2**64-2)]:
        result = (x-y)%(2**64)
        result = bin(result)[2:]
        x_bin = bin(x)[2:]
        while len(x_bin) < 64:
            x_bin = '0'+x_bin
        y_bin = bin(y)[2:]
        while len(y_bin) < 64:
            y_bin = '0'+y_bin
        test_mpc(t, n, c_path, n_triples, [x_bin[::-1], y_bin[::-1]], result)

def test_mul2_circuit():
    t = 2
    n = 5
    c_path = "bristol_circuits/mul2.txt"
    n_triples = 500
    for x,y in [(0,1), (0,0), (1,1)]:
        result = (x*y)
        result = bin(result)[2:]
        x_bin = bin(x)[2:]
        y_bin = bin(y)[2:]
        test_mpc(t, n, c_path, n_triples, [x_bin, y_bin], result)

def test_mul64mod_circuit():
    t = 2
    n = 5
    c_path = "bristol_circuits/mul64mod.txt"
    n_triples = 10000
    for x,y in [(111, 2025), (2**64-1, 2**64-1)]:
        result = bin((x*y)%(2**64))[2:]
        x_bin = bin(x)[2:]
        while len(x_bin) < 64:
            x_bin = '0'+x_bin
        y_bin = bin(y)[2:]
        while len(y_bin) < 64:
            y_bin = '0'+y_bin
        test_mpc(t, n, c_path, n_triples, [x_bin[::-1], y_bin[::-1]], result)

def test_mul64_circuit():
    t = 2
    n = 5
    c_path = "bristol_circuits/mul64.txt"
    n_triples = 10000
    for x,y in [(111, 2025), (2**64-1, 2**64-1)]:
        result = bin((x*y))[2:]
        x_bin = bin(x)[2:]
        while len(x_bin) < 64:
            x_bin = '0'+x_bin
        y_bin = bin(y)[2:]
        while len(y_bin) < 64:
            y_bin = '0'+y_bin
        test_mpc(t, n, c_path, n_triples, [x_bin[::-1], y_bin[::-1]], result, reflect=True)

def test_lessthan32_circuit():
    t = 2
    n = 5
    c_path = "bristol_circuits/lessthan32.txt"
    n_triples = 10000
    for x,y in [(111, 2025), (2025, 111), (2**32-1, 2**32-1)]:
        result = bin(x<y)[2:]
        x_bin = bin(x)[2:]
        while len(x_bin) < 32:
            x_bin = '0'+x_bin
        y_bin = bin(y)[2:]
        while len(y_bin) < 32:
            y_bin = '0'+y_bin
        test_mpc(t, n, c_path, n_triples, [x_bin[::-1], y_bin[::-1]], result)

if __name__ == "__main__":
    print("--BEGIN ADD64 TEST--")
    test_add64_circuit()
    print("--BEGIN SUB64 TEST--")
    test_sub64_circuit()
    print("--BEGIN LT32 TEST--")
    test_lessthan32_circuit()
    print("--BEGIN MUL2 TEST--")
    test_mul2_circuit()
    print("--BEGIN MUL64MOD TEST--")
    test_mul64mod_circuit()
    print("--BEGIN MUL64 TEST--")
    test_mul64_circuit()
