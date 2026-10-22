"""Tonelli-Shanks square root modulo a prime."""


def _legendre(a: int, p: int) -> int:
    """Compute the Legendre symbol (a/p) via Euler's criterion.

    Returns 0 when a is divisible by p, 1 when a is a quadratic residue,
    and -1 when it is a non-residue. Euler's criterion is used because it is
    a one-shot modular exponentiation; no factorisation of p is needed.
    """
    if a % p == 0:
        return 0
    result = pow(a, (p - 1) // 2, p)
    # pow returns a non-negative residue, so a result of p-1 means -1.
    if result == p - 1:
        return -1
    return result


def is_quadratic_residue(a: int, p: int) -> bool:
    """Return True iff a is a quadratic residue modulo the odd prime p.

    Uses the Legendre symbol, so this shares the same modular exponentiation
    path as modular_sqrt and gives consistent answers.
    """
    if p < 3:
        raise ValueError("p must be an odd prime")
    if p == 2:
        raise ValueError("p must be an odd prime")
    a = a % p
    if a == 0:
        return True
    return _legendre(a, p) == 1


def modular_sqrt(a: int, p: int):
    """Return a square root of a modulo the odd prime p, or None.

    Implements the Tonelli-Shanks algorithm. If a is a non-residue, None is
    returned. If a is 0 mod p, 0 is returned. The returned root is always the
    smaller of the two roots (r and p-r) where applicable; both square to a.

    p must be an odd prime. p == 2 is rejected with ValueError.
    """
    if p < 3:
        raise ValueError("p must be an odd prime")
    if p == 2:
        raise ValueError("p must be an odd prime")

    a = a % p

    if a == 0:
        return 0

    # Reject non-residues up front so the caller gets None rather than a
    # meaningless answer from the algorithm below.
    if _legendre(a, p) != 1:
        return None

    # Fast path: p ≡ 3 (mod 4). The root is a^((p+1)/4), a single pow call.
    if p % 4 == 3:
        r = pow(a, (p + 1) // 4, p)
        return min(r, p - r)

    # General Tonelli-Shanks. Decompose p-1 = 2^e * q with q odd.
    q = p - 1
    e = 0
    while q % 2 == 0:
        q //= 2
        e += 1

    # Find a non-residue z to use as the generator of the 2-Sylow subgroup.
    # A random search would also work, but a deterministic scan from 2 keeps
    # behaviour reproducible and avoids a source of randomness.
    z = 2
    while _legendre(z, p) != -1:
        z += 1

    m = e
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)

    while t != 1:
        # Find the least i, 0 < i < m, such that t^(2^i) ≡ 1.
        i = 0
        temp = t
        while temp != 1:
            temp = (temp * temp) % p
            i += 1
            if i == m:
                # Should be unreachable because a is a residue; kept as a guard.
                return None

        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = (b * b) % p
        t = (t * c) % p
        r = (r * b) % p

    return min(r, p - r)
