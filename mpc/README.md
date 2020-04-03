# Multi Pary Computation

[What is Secure Multi Party Computation?](https://en.wikipedia.org/wiki/Secure_multi-party_computation)

## Demo SafetraceMPC

### Local demo

To locally demo/test the package open two terminals.

In the first terminal enter the safetraceapi/mpc directory and run `python3 local_mpc_network.py`. This spawns a 3 node MPC network on your local machine.
In the second terminal enter the safetraceapi/mpc directory and run `python3 mpc_test.py`. This spawns two clients which both send a request to the MPC servers with a secret shared integer as input. The MPC servers compute whether or not the integers "intersect" (are within a range of 1000) without ever revealing the two integers, and return the results which the clients can locally 'decrypt'

### Live demo

We've set up a simple demo on a virtual machine partitioned into 3 separate servers. Enter the safetraceapi/mpc directory and run demo.py choosing an integer and a string as command line arguments. Then have a friend (or you in a separate shell) do the same. The two calls should look like this:

```
// request 1
$ python3 demo.py 1234 abc

// request 2
$ python3 demo.py 55555 abc
```

The final string must be a matching unique reference id so the servers know that these two requests go together. The servers will compute the "intersection" between the two integers without ever decrypting or leaking any information about these integers (though the connections should be SSL and are simple unencrypted TCP for now, which could potentially leak information).

The servers are not very sophisticated so I won't be surprised if some requests get stuck (though you'll certainly wait forever regardless if the second client never sends a request with a matching string argument). ALso they are on free tier AWS and all three share one VM which means performance is certainly diminished.

## Package Overview

This Multi Party Computation implementation relies on a number of classes:

1. `Node` class: An MPC node with a predefied set of peers (see: node.py)
2. `Client` class: A client that can query the MPC nodes with MPC operations (see: client.py)
3. `Circuit` class: A boolean circuit evaluator (see: circuit.py)
4. `Shamir` class: Shamir Secret Sharing over field GF256 (see: shamir.py)
5. `Messenger` class: the interface between the main circuit evaluation process, and the processes handling p2p communication.

## Circuits

The `Circuit` class is instanciated with two arguments, a path to a bytecode file and a list of input types:
- Bytecode Files are loaded from 'Bristol Fashion' txt files. Learn more about the bytecode format here: https://homes.esat.kuleuven.be/~nsmart/MPC/
- Input types are a list of 'V' or 'S' characters where 'S' stands for share and 'V' for value (i.e. a plaintext bit).

The `Circuit` class is made to work in such a way that if only plaintext bits are passed as inputs to the `Circuit` then it can be evaluated 100% locally (the `Circuit` class becomes a simple program executor). However if secret shared bits are passed to the `Circuit` a successful result can only be obtained if a distrbuted set of parties D all run the `Circuit` in parallel (each with their corresponding shares as inputs) where D must be greater than t+1 (and t is the degree of the polynomial from which the secret shares are sampled). When the share outputs are brought together and reconstructed, the correct value of the computation is finally revealed.

A messenger class is only necessary if communication is necessary given the circuit and input types (communication is necessary for any AND gate that takes two share values as input).

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