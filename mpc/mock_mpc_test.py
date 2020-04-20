from circuit import Circuit, RuntimeCircuit
from shamir import Shamir
from mock_triples import gen_triples
from mock_messaging import MockMessenger
from multiprocessing import Queue, Process
import time

def consumer(mq, n, result, t, processes, reflect):
    vals = []
    while len(vals) < t+1:
        if not mq.empty():
            vals.append(mq.get())
    reconstructed = Shamir(t, n).reconstruct_bitstring_secret(vals)[::-1]
    if reflect:
        reconstructed = reconstructed[int(len(reconstructed)/2):]+reconstructed[:int(len(reconstructed)/2)]
    assert eval('0b'+reconstructed) == eval('0b'+result), "result incorrect"

def run_circuit_process(t, n, c, index, queues, main_queue, inputs, triples):
    shamir = Shamir(t, n)
    messenger = MockMessenger(t, n, index, queues, "--UNIQUE COMPUTATION ID--")
    runtime = RuntimeCircuit(c, inputs, triples=triples, shamir=shamir)
    outputs = runtime.evaluate(messenger)
    main_queue.put(outputs)

<<<<<<< HEAD
def run_circuit_process(t, n, c, index, queues, main_queue, inputs, triples):
    asyncio.run(eval_circuit(t, n, c, index, queues, main_queue, inputs, triples))

def test_mpc(t, n, c_path, n_triples, all_inputs, result, reflect=False):
    triples = gen_triples(t, n, n_triples)
=======
def test_mpc(t, n, c_path, triples, all_inputs, result, reflect=False):
>>>>>>> upstream/master
    mq = Queue()
    queues = [Queue() for _ in range(n)]
    processes = []
    itypes = []
    for i in all_inputs[0]:
        if i in [0, 1]:
            itypes.append('V')
        else:
            itypes.append('S')
    c = Circuit(c_path, itypes)
    for i in range(n):
        p = Process(target=run_circuit_process, args=(t, n, c, i+1, queues, mq, all_inputs[i], triples[i]))
        processes.append(p)
    start = time.time()
    for p in processes:
        p.start()
    t1 = Process(target=consumer, args=(mq, n, result, t, processes, reflect))
    t1.start()
    t1.join()
    for p in processes:
        p.terminate()
    print(f"time: {round(time.time()-start, 4)} seconds")
    while not mq.empty():
        mq.get()
    mq.close()
    for q in queues:
        q.close()
        q.join_thread()
    mq.join_thread()

def test_add64_circuit(t, n, triples):
    c_path = "bristol_circuits/add64.txt"
    for x,y in [(100, 200), (2**30, 2**10), (2**64-1, 2**64-1)]:
        result = bin((x+y)%(2**64))[2:]
        x_bin = bin(x)[2:]
        while len(x_bin) < 64:
            x_bin = '0'+x_bin
        y_bin = bin(y)[2:]
        while len(y_bin) < 64:
            y_bin = '0'+y_bin
        inputs = Shamir(t, n).share_bitstring_secret(x_bin[::-1]+y_bin[::-1])
<<<<<<< HEAD
        test_mpc(t, n, c_path, n_triples, inputs, result)
=======
        test_mpc(t, n, c_path, triples, inputs, result)
>>>>>>> upstream/master

def test_sub64_circuit(t, n, triples):
    c_path = "bristol_circuits/sub64.txt"
    for x,y in [(1000, 2010), (2025, 111), (2**64-2, 2**64-2)]:
        result = (x-y)%(2**64)
        result = bin(result)[2:]
        x_bin = bin(x)[2:]
        while len(x_bin) < 64:
            x_bin = '0'+x_bin
        y_bin = bin(y)[2:]
        while len(y_bin) < 64:
            y_bin = '0'+y_bin
        inputs = Shamir(t, n).share_bitstring_secret(x_bin[::-1]+y_bin[::-1])
<<<<<<< HEAD
        test_mpc(t, n, c_path, n_triples, inputs, result)
=======
        test_mpc(t, n, c_path, triples, inputs, result)
>>>>>>> upstream/master

def test_mul2_circuit(t, n, triples):
    c_path = "bristol_circuits/mul2.txt"
<<<<<<< HEAD
    n_triples = 2
=======
>>>>>>> upstream/master
    for x,y in [(0,1), (0,0), (1,1)]:
        result = (x*y)
        result = bin(result)[2:]
        x_bin = bin(x)[2:]
        y_bin = bin(y)[2:]
        inputs = Shamir(t, n).share_bitstring_secret(x_bin+y_bin)
<<<<<<< HEAD
        test_mpc(t, n, c_path, n_triples, inputs, result)
=======
        test_mpc(t, n, c_path, triples, inputs, result)
>>>>>>> upstream/master

def test_mul64mod_circuit(t, n, triples):
    c_path = "bristol_circuits/mul64mod.txt"
    for x,y in [(111, 2025), (2**64-1, 2**64-1)]:
        result = bin((x*y)%(2**64))[2:]
        x_bin = bin(x)[2:]
        while len(x_bin) < 64:
            x_bin = '0'+x_bin
        y_bin = bin(y)[2:]
        while len(y_bin) < 64:
            y_bin = '0'+y_bin
        inputs = Shamir(t, n).share_bitstring_secret(x_bin[::-1]+y_bin[::-1])
<<<<<<< HEAD
        test_mpc(t, n, c_path, n_triples, inputs, result)
=======
        test_mpc(t, n, c_path, triples, inputs, result)
>>>>>>> upstream/master

def test_mul64_circuit(t, n, triples):
    c_path = "bristol_circuits/mul64.txt"
    for x,y in [(111, 2025), (2**64-1, 2**64-1)]:
        result = bin((x*y))[2:]
        x_bin = bin(x)[2:]
        while len(x_bin) < 64:
            x_bin = '0'+x_bin
        y_bin = bin(y)[2:]
        while len(y_bin) < 64:
            y_bin = '0'+y_bin
        inputs = Shamir(t, n).share_bitstring_secret(x_bin[::-1]+y_bin[::-1])
<<<<<<< HEAD
        test_mpc(t, n, c_path, n_triples, inputs, result, reflect=True)
=======
        test_mpc(t, n, c_path, triples, inputs, result, reflect=True)
>>>>>>> upstream/master

def test_lessthan32_circuit(t, n, triples):
    c_path = "bristol_circuits/lessthan32.txt"
    for x,y in [(111, 2025), (2025, 111), (2**32-1, 2**32-1)]:
        result = bin(x<y)[2:]
        x_bin = bin(x)[2:]
        while len(x_bin) < 32:
            x_bin = '0'+x_bin
        y_bin = bin(y)[2:]
        while len(y_bin) < 32:
            y_bin = '0'+y_bin
        inputs = Shamir(t, n).share_bitstring_secret(x_bin[::-1]+y_bin[::-1])
<<<<<<< HEAD
        test_mpc(t, n, c_path, n_triples, inputs, result)

def test_unnormalized_example():
    t = 1
    n = 3
    c_path = "bristol_circuits/unnormalized_subregion_100_10.txt"
    n_triples = 200000
    ones = ['1' for _ in range(1200)]
    inputs = Shamir(t, n).share_bitstring_secret(ones)
    for i in range(len(inputs)):
        inputs[i] = [0 for _ in range(64)]+inputs[i]
    result = bin(300)[2:]
    while len(result)<64:
        result = '0'+result
    result = result*10
    test_mpc(t, n, c_path, n_triples, inputs, result)
=======
        test_mpc(t, n, c_path, triples, inputs, result)

def test_unnormalized_subregion_10k(t, n, triples):
    c_path = "bristol_circuits/unnormalized_subregion_10000_1.txt"
    ones = ['1' for _ in range(30000)]
    inputs = Shamir(t, n).share_bitstring_secret(ones)
    for i in range(len(inputs)):
        inputs[i] = [0 for _ in range(64)]+inputs[i]
    result = bin(30000)[2:]
    while len(result)<64:
        result = '0'+result
    result = result
    test_mpc(t, n, c_path, triples, inputs, result)
>>>>>>> upstream/master

if __name__ == "__main__":
    t=1
    n=3
    triples = gen_triples(t, n, 10000)
    print("--BEGIN MUL2 TEST--")
    n_triples = 1
    test_mul2_circuit(t, n, [tr[:n_triples] for tr in triples])
    print("--BEGIN ADD64 TEST--")
    n_triples=500
    test_add64_circuit(t, n, [tr[:n_triples] for tr in triples])
    print("--BEGIN SUB64 TEST--")
    test_sub64_circuit(t, n, [tr[:n_triples] for tr in triples])
    print("--BEGIN LT32 TEST--")
    n_triples = 10000
    test_lessthan32_circuit(t, n, [tr[:n_triples] for tr in triples])
    print("--BEGIN MUL64MOD TEST--")
    test_mul64mod_circuit(t, n, [tr[:n_triples] for tr in triples])
    print("--BEGIN MUL64 TEST--")
<<<<<<< HEAD
    test_mul64_circuit()
    print("--BEGIN LONG TEST--")
    test_unnormalized_example()
=======
    test_mul64_circuit(t, n, [tr[:n_triples] for tr in triples])
    print("--BEGIN LONG TEST--")
    print("initializing triples...")
    start = time.time()
    triples = gen_triples(1, 3, 1000000)
    print(f"time: {round(time.time()-start, 4)}")
    test_unnormalized_subregion_10k(t, n, triples)
>>>>>>> upstream/master
