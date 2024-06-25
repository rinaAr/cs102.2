import random
from typing import Tuple

def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a

def multiplicative_inverse(e: int, phi: int) -> int:
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        g, y, x = extended_gcd(b % a, a)
        return g, x - (b // a) * y, y

    g, x, y = extended_gcd(e, phi)
    return x % phi

def generate_keypair(p: int, q: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = multiplicative_inverse(e, phi)

    return ((e, n), (d, n))
