#!/usr/bin/env python
import unittest
import primes
from array import array

__author__ = "Jerome Migne"
__copyright__ = "Copyright 2018, Jerome Migne"
__license__ = "GPLv3"


class TestPrimes(unittest.TestCase):

    def test_sieve(self):
        self.assertEqual(len(primes.build_sieve(-2)), 0)
        self.assertEqual(len(primes.build_sieve(-1)), 0)
        self.assertSequenceEqual(primes.build_sieve(0), [0])
        self.assertSequenceEqual(primes.build_sieve(1), [0, 0])
        self.assertSequenceEqual(primes.build_sieve(2), [0, 0, 1])
        self.assertSequenceEqual(
            primes.build_sieve(30),
            [0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0,
             0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0])
        a = primes.build_sieve(65538)
        self.assertSequenceEqual(a[65536:65539], [0, 1, 0])

    def _test_gen_primes(self, gen, expecteds):
        n = len(expecteds)
        count = 0
        for p in gen:
            self.assertLess(count, n)
            self.assertEqual(p, expecteds[count], "count: " + str(count))
            count += 1
        self.assertEqual(count, n)

    def test_gen_primes_from_sieve(self):
        self._test_gen_primes(
            primes.gen_primes_from_sieve(primes.build_sieve(1)),
            [])
        self._test_gen_primes(
            primes.gen_primes_from_sieve(primes.build_sieve(30)),
            [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])

    def _test_estimate_nth_prime(self, n, p):
        ret = primes.estimate_nth_prime(n)
        self.assertLessEqual(ret[0], p)
        self.assertGreaterEqual(ret[1], p)

    def test_estimate_nth_prime(self):
        self.assertRaises(ValueError, primes.estimate_nth_prime, 0)
        self.assertRaises(ValueError, primes.estimate_nth_prime, 1.5)
        self._test_estimate_nth_prime(1, 2)
        self._test_estimate_nth_prime(2, 3)
        self._test_estimate_nth_prime(3, 5)
        self._test_estimate_nth_prime(4, 7)
        self._test_estimate_nth_prime(5, 11)
        self._test_estimate_nth_prime(6, 13)
        self._test_estimate_nth_prime(7, 17)
        self._test_estimate_nth_prime(8, 19)
        self._test_estimate_nth_prime(9, 23)
        self._test_estimate_nth_prime(10, 29)
        self._test_estimate_nth_prime(20, 71)
        self._test_estimate_nth_prime(100, 541)
        self._test_estimate_nth_prime(1000, 7919)
        self._test_estimate_nth_prime(10000, 104729)
        self._test_estimate_nth_prime(100000, 1299709)
        self._test_estimate_nth_prime(1000000, 15485863)

    def test_gen_first_primes(self):
        self._test_gen_primes(
            primes.gen_first_primes(10),
            [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])

    def test_wheel(self):
        w = primes.Wheel(3)
        self.assertAlmostEqual(w.ratio, 0.2666667)
        gen = w.gen_divisors()
        d = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53,
             59, 61, 67, 71, 73, 77, 79, 83, 89, 91]
        for k in d:
            self.assertEqual(next(gen), k)

    def test_factorize(self):
        self.assertEqual(primes.factorize(0), [])
        self.assertEqual(primes.factorize(1), [])
        self.assertEqual(primes.factorize(2), [(2, 1)])
        self.assertEqual(primes.factorize(10), [(2, 1), (5, 1)])
        self.assertEqual(primes.factorize(45), [(3, 2), (5, 1)])
        self.assertEqual(primes.factorize(5000), [(2, 3), (5, 4)])
        self.assertEqual(primes.factorize(65537), [(65537, 1)])
        self.assertEqual(primes.factorize(5 * 11**3 * 65537**2),
                         [(5, 1), (11, 3), (65537, 2)])


if __name__ == '__main__':
    unittest.main()
