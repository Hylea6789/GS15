from prime_numbers import *
import unittest


class PrimeNumberGeneratorTest(unittest.TestCase):
    @staticmethod
    def is_prime(nbr) -> bool:
        """
        On vérifie que le nombre est premier avec la méthode
        déterministe traditionnelle.
        C'est plus lent que Rabin-Miller, mais un test, c'est
        fait pour être correct, pas rapide.
        """
        if nbr % 2 == 0:
            return False
        return all((nbr % i) != 0 for i in range(3, nbr, 2))

    def test(self):
        for _ in range(10):
            res = gen_nbr_premier(1_000_000)
            self.assertTrue(self.is_prime(res))
