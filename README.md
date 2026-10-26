# simple-modular-square-root

Computes square roots modulo an odd prime using the Tonelli-Shanks algorithm, returning `None` for quadratic non-residues.

```python
from simple_modular_square_root import modular_sqrt, is_quadratic_residue

r = modular_sqrt(2, 7)   # returns 3, since 3*3 = 9 ≡ 2 (mod 7)
modular_sqrt(5, 7)       # returns None — 5 is a non-residue mod 7
is_quadratic_residue(2, 7)  # True
is_quadratic_residue(5, 7)  # False
```

## Why this exists

The Tonelli-Shanks algorithm is the standard general-purpose method for computing square roots modulo a prime. It runs in polynomial time for any odd prime, with a fast path (`a^((p+1)/4)`) when `p ≡ 3 (mod 4)`. This library implements that algorithm with no external dependencies, returning `None` for non-residues so callers can branch on the result without catching exceptions.

The trade-off: input validation checks that `p` is odd and greater than 2, but does **not** prove primality. Passing a composite `p` may produce incorrect results silently. The caller is responsible for ensuring `p` is prime.

## Edge cases

- `a ≡ 0 (mod p)` returns `0`.
- `a` larger than `p` is reduced automatically.
- `p = 2` and `p < 3` raise `ValueError`. Tonelli-Shanks requires an odd prime; the case `p = 2` is excluded rather than special-cased to keep the contract simple.
- The returned root is the smaller of the two square roots (`r` and `p - r`), so results are deterministic.

## Exports

- `modular_sqrt(a, p)` — returns `int` or `None`.
- `is_quadratic_residue(a, p)` — returns `bool`.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

