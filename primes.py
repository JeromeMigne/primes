"""Module for prime numbers computations.
Implements some basic algorithms:
    sieve of Eratosthenes,
    estimation of nth prime,
    wheel factorization.
"""
from array import array
import math
import sys

__author__ = "Jerome Migne"
__copyright__ = "Copyright 2018, Jerome Migne"
__license__ = "GPLv3"

if sys.version_info < (3,):
    range = xrange


def build_sieve(bound):
    """Build a sieve of Eratosthenes.

    Arguments
    ---------
    bound : int
        Upper inclusive bound of the sieve.

    Returns
    -------
    array
        Bytes array of `bound` + 1 elements whose value at index i is:
            0 if i is not prime
            1 if i is prime
    """
    bound = int(bound)
    a = array('B', (0 for i in range(min(2, bound + 1))))
    a.extend((1 for i in range(2, bound + 1)))
    for i in range(2, int(math.sqrt(max(0, bound))) + 1):
        if a[i]:
            for j in range(i * i, bound + 1, i):
                a[j] = 0
    return a


def gen_primes_from_sieve(sieve):
    """Generator of prime numbers from a sieve."""
    for i in range(2, len(sieve)):
        if sieve[i]:
            yield i


def estimate_nth_prime(n):
    """Give an estimation of the nth prime.

    Arguments
    ---------
    n : int
        order number of the prime to estimate the value

    Returns
    -------
    tuple of 2 elements: inclusive lower and upper bounds
    of the value of `n`th prime.

    References
    ----------
    https://www.ams.org/journals/mcom/1999-68-225/S0025-5718-99-01037-6/S0025-5718-99-01037-6.pdf
    """
    if n != int(n) or n <= 0:
        raise ValueError("n should be a positive integer")
    if n == 1:
        return (2, 2)
    x = n * (math.log(n) + math.log(math.log(n)))
    return (math.ceil(x) - n, math.floor(x) if n >= 6 else 11)


def gen_first_primes(count):
    """Generator of first `count` primes."""
    bound = estimate_nth_prime(count)[1]
    for p in gen_primes_from_sieve(build_sieve(bound)):
        if count <= 0:
            break
        count -= 1
        yield p


class Wheel:
    """Allow to generate divisors not multiple of any primes of a basis."""

    def __init__(self, n):
        """Wheel initialization.

        Arguments
        ---------
        n : int
            number of primes in the basis
        """
        if n < 1:
            raise ValueError("n should be greater or equal than 1")
        self._basis = array('I', (p for p in gen_first_primes(n)))
        basis_end = self._basis[-1] + 1
        period = self._get_period()
        first_round_end = period + 2
        a = array('B', (1 for i in range(first_round_end)))
        for p in self._basis:
            for k in range(max(p * p, basis_end), first_round_end, p):
                a[k] = 0
        self._increments = array('I')
        cur = None
        for k in range(basis_end, first_round_end):
            if a[k]:
                if cur is None:
                    self._first_spoke = k
                else:
                    self._increments.append(k - cur)
                cur = k
        self._increments.append(self._first_spoke + period - cur)

    def _get_period(self):
        res = 1
        for p in self._basis:
            res *= p
        return res

    @property
    def ratio(self):
        """Ratio of generated divisors with respect to generate all numbers."""
        return len(self._increments) * 1.0 / self._get_period()

    def gen_divisors(self):
        """Generator of divisors that can be used for factorization."""
        for p in self._basis:
            yield p
        k = self._first_spoke
        yield k
        while True:
            for inc in self._increments:
                k += inc
                yield k


_default_wheel = Wheel(4)

def factorize(n, wheel=_default_wheel):
    """Factorize a number into prime factors.

    Use wheel factorization algorithm which is an improvement of trial
    divisions algorithm. Divisors are generated from a wheel that allows to
    reduce the number of divisions.

    Arguments
    ---------
    n : int
        Number to factorize.
    wheel : optional
        Wheel object used to generate divisors. Allow to tune the algorithm.

    Returns
    -------
    List of pairs whose first value is a prime factor of `n`
    and second value is the exponent applied to this factor.
    The list is ordered in ascending order of the factors.
    When the input `n` is prime, the returned list is [(`n`, 1)]

    References
    ----------
    https://en.wikipedia.org/wiki/Wheel_factorization
    """
    factors = []
    cur = [0, 0]
    for k in wheel.gen_divisors():
        if k * k > n:
            break
        while True:
            q, r = divmod(n, k)
            if r:
                break
            n = q
            if k != cur[0]:
                cur = [k, 1]
                factors.append(cur)
            else:
                cur[1] += 1
    if n > 1:
        factors.append([n, 1])
    return [(item[0], item[1]) for item in factors]
