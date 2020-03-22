# Multi Pary Computation

https://en.wikipedia.org/wiki/Secure_multi-party_computation

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