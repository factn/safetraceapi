# Multi Party Computation

[What is Secure Multi Party Computation?](https://en.wikipedia.org/wiki/Secure_multi-party_computation)

## Requirements

- python 3.7+
- gf256 module (`pip3 install gf256`)

## Demo SafetraceMPC

The SafetraceMPC demo is a *privacy preserving* geolocal intersection.  Choose any standard decimal degree geolocation on the globe and our MPC servers will evaluate whether or not the coordinate falls within Brooklyn, NY. The servers compute this intersection **without ever having access to the client's actual geo-coordinate or leakng any information about it**. The servers do not even learn the result of the computation (only the client can reconstruct the result bit from each of the servers partial results)

To run the demo enter the safetrace/mpc directory. Run the demo and pass the latitude and longitude as options like so:

```
$ python3 mpc_demo.py -lat 40.635 -lon -73.981 
```

Note that since the server-client connections are not using TLS (and a few other details, like the reuse of multiplication triples) this is for demo purposes only and NOT FULLY SECURED.

### Local demo

To locally demo/test the package open two shell sessions. In the safetrace/mpc directory run:

```
// shell 1
$ python3 local_mpc_network.py

// shell 2
$ python3 local_mpc_test.py
```


- `local_mpc_network.py`: This spawns a 3 node MPC network on your local machine.
- `local_mpc_test.py`: This spawns a client to query the server with goelocal coordinates, locally running the same secure computation as in the 'live' demo above.

## Package Overview

This Multi Party Computation implementation relies on a number of classes:

1. `Server` class: An MPC node with a predefied set of peers (see: node.py)
2. `Client` class: A client that can query the MPC nodes with MPC operations (see: client.py)
3. `Circuit` class: A boolean circuit evaluator (see: circuit.py)
4. `Shamir` class: Shamir Secret Sharing over field GF256 (see: shamir.py)
5. `Dispatcher` class: the interface between the main circuit evaluation process, and the processes handling p2p communication.

## Circuits

The `Circuit` class is instanciated with two arguments, a path to a bytecode file and a list of input types:
- Bytecode Files are loaded from 'Bristol Fashion' txt files. Learn more about the bytecode format here: https://homes.esat.kuleuven.be/~nsmart/MPC/
- Input types are a list of 'V' or 'S' characters where 'S' stands for share and 'V' for value (i.e. a plaintext bit).

The `Circuit` class is made to work in such a way that if only plaintext bits are passed as inputs to the `Circuit` then it can be evaluated 100% locally (the `Circuit` class becomes a simple program executor). However if secret shared bits are passed to the `Circuit` a successful result can only be obtained if a distrbuted set of parties D all run the `Circuit` in parallel (each with their corresponding shares as inputs) where D must be greater than t+1 (and t is the degree of the polynomial from which the secret shares are sampled). When the share outputs are brought together and reconstructed, the correct value of the computation is finally revealed.

A dispatcher class is only necessary if communication is necessary given the circuit and input types (communication is necessary for any AND gate that takes two share values as input).

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