# Multi Party Computation

[What is Secure Multi Party Computation?](https://en.wikipedia.org/wiki/Secure_multi-party_computation)

## Requirements

- python 3.7+
- gf256 module (`pip3 install gf256`)
- aiohttp module (`pip3 install aiohttp, cchardet, aiodns`)

## Clone and test

<<<<<<< HEAD
The SafetraceMPC demo is a *privacy preserving* geolocal intersection.  Choose any standard decimal degree geolocation on the globe and our MPC servers will evaluate whether or not the coordinate falls within Brooklyn, NY. The servers compute this intersection **without ever having access to the client's actual geo-coordinate or leakng any information about it**. The servers do not even learn the result of the computation (only the client can reconstruct the result bit from each of the servers partial results)
=======
Clone the root repository and enter the mpc directory. 
>>>>>>> upstream/master

Before running tests make sure to unzip any zipped files in the `bristol_circuits` directory (some tests will fail if not).

Test files are any python files that end with `..._test.py`. Run them as you'd run any python file (`$ python3 <filename>`). They each test individual components of the MPC engine.

## Integration Test

We do not currently have proper integration testing (in general we can still improve testing across this project). To quickly verify that the entire platform runs properly run these three commands (in three processes, simultaneously):

```
$ python3 runtriples.py 8000 1 3 1 '[("127.0.0.1", 8001, 2), ("127.0.0.1", 8002, 3)]'
$ python3 runtriples.py 8001 1 3 2 '[("127.0.0.1", 8000, 1), ("127.0.0.1", 8002, 3)]'
$ python3 runtriples.py 8002 1 3 3 '[("127.0.0.1", 8000, 1), ("127.0.0.1", 8001, 2)]'
```

this should start generating triples with coordinated prints to the std out every few seconds in each terminal.

## Package Overview

This Multi Party Computation implementation relies on a number of classes:

1. `MPCPeer` class: An MPC node with a predefied set of peers (see: mpc.py)
3. `Circuit` class: A boolean circuit evaluator (see: circuit.py)
4. `Shamir` class: Shamir Secret Sharing over field GF256 (see: shamir.py)

## Circuits

The `Circuit` class is instanciated with two arguments, a path to a bytecode file and a list of input types:
- Bytecode Files are loaded from 'Bristol Fashion' txt files. Learn more about the bytecode format here: https://homes.esat.kuleuven.be/~nsmart/MPC/
- Input types are a list of 'V' or 'S' characters where 'S' stands for share and 'V' for value (i.e. a plaintext bit).

You can verify that an MPC circuit compiled in the Bristol Fashion works properly by instanciating and evaluating an instance of this circuit with only plaintext inputs (see input types above). Without share inputs a `Circuit` operates as an entirely local bytecode evaluator.

## Shamir Secret Sharing 

The `Shamir` class is a set of methods for a secure (t, n) secret sharing scheme where any t+1 out of n total shares are needed to reconstruct a secret value. The scheme works over the field GF(2^8) for it's applicability to muilti party computtaion with boolean circuits.

```
>>> from shamir import Shamir
>>> shamir = Shamir(2,5)
>>> shares = shamir.share_secret(15)
>>> shares
[(1, 168), (2, 169), (3, 14), (4, 185), (5, 30)]
>>> int(shamir.recontsruct_secret(shares[:3]))
15
>>> shares = shamir.share_bitstring_secret('10010101010010')
>>> shamir.reconstruct_bitstring_secret(shares[2:])
'10010101010010'
```

### Homomorphisms of Shamir Secret Sharing

Shamir Secret Sharing as *linearly* homomorphic out of the box. If each player in the MPC protocol takes an index [1,..,n] and gets their share [x] of secret value x and [y] of secret value y, they can locally combine their shares to get a share [x+y]. Here's proof below:

```
>>> from gf256 import GF256
>>> from shamir import Shamir
>>> x = GF256(1)
>>> y = GF256(2)
>>> shamir = Shamir(2,5)
>>> x_shares = shamir.share_secret(x)
>>> y_shares = shamir.share_secret(y)
>>> result_shares = [x_shares[i]+y_shares[i] for i in range(len(x_shares))]
>>> shamir.reconstruct_secret(result_shares[:3]) == x+y
True
```

Linear homomorphism also means that a secret shared value x may be multiplied by a public value c with simple local computations (by all parties). Each player with share [x] can do c\*[x] to obtain a share [c\*x].

```
>>> from gf256 import GF256
>>> from shamir import Shamir
>>> x = GF256(25)
>>> c = GF256(3)
>>> shamir = Shamir(2,5)
>>> x_shares = shamir.share_secret(x)
>>> result_shares = [share.scalar_mul(c) for share in x_shares]
>>> shamir.reconstruct_secret(result_shares[:3]) == c*x
True
```

Shamir Secret Sharing is similarly *multiplicatively* homomorphic EXCEPT that the threshold number of shares needed for reconstruction doubles after every multiplication. To mitigate this problem there is a preprocessing phase to create a "TripleShare" three values [a],[b],[c] where secret values a,b,c have relationship a\*b=c.

Players first compute:
```
[epsilon] = [x-a]
[rho] = [y-b]
```

Then they broadcast shares [epsilon] and [rho] to all other parties. Players then compute result share [r]:

```
epsilon = reconstruct([epsilon]_1, [epsilon_2]...)
rho = reconstruct([rho]_1, [rho]_2...)
[r] = rho*[x] + epsilon*[y] - epsilon\*rho
[r] = [(y-b)*x] + [(x-a)*y] - (x-a)*(y-b) + c
[r] = [(xy-xb) + (xy-ya) - (xy-ya-xb+ab) + ab]
[r] = [xy]
```

With this protocol (involving one round of communication and pre-created TripleShares) we can compute multiplications homomorphically in the secret shared space. Proof of this can be seen in test_secure_multiplication() in the test file shamir_test.py