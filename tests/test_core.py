import unittest

from simple_modular_square_root import modular_sqrt, is_quadratic_residue


class TestModularSqrt(unittest.TestCase):
    def test_non_residue_returns_none(self):
        # 5 is a non-residue mod 7: 1^2..6^2 mod 7 give {1,2,4}.
        self.assertIsNone(modular_sqrt(5, 7))

    def test_zero(self):
        self.assertEqual(modular_sqrt(0, 7), 0)

    def test_small_prime_p3_mod4_fast_path(self):
        # 7 ≡ 3 mod 4. 2 is a residue: 3^2 = 9 ≡ 2.
        r = modular_sqrt(2, 7)
        self.assertEqual((r * r) % 7, 2)
        # We return the smaller of the two roots.
        self.assertEqual(r, 3)

    def test_small_prime_p1_mod4_general_case(self):
        # 5 ≡ 1 mod 4. 4 is trivially a residue; root is 2 (and 3).
        r = modular_sqrt(4, 5)
        self.assertEqual((r * r) % 5, 4)
        self.assertEqual(r, 2)

    def test_residue_p1_mod4_non_trivial(self):
        # 13 ≡ 1 mod 4. Squares mod 13: {1,3,4,9,10,12}.
        # 3 is a residue (4^2 = 16 ≡ 3).
        r = modular_sqrt(3, 13)
        self.assertIsNotNone(r)
        self.assertEqual((r * r) % 13, 3)

    def test_returns_smaller_root(self):
        # Roots of 2 mod 7 are 3 and 4. We return 3.
        self.assertEqual(modular_sqrt(2, 7), 3)

    def test_large_prime_fast_path(self):
        # 2^31 - 1 is prime and ≡ 3 mod 4.
        p = 2147483647
        a = 2
        r = modular_sqrt(a, p)
        self.assertIsNotNone(r)
        self.assertEqual((r * r) % p, a % p)

    def test_large_prime_general_case(self):
        # A 5 ≡ 1 mod 4 prime: 2^16 + 1 = 65537 (Fermat prime).
        p = 65537
        a = 12345
        r = modular_sqrt(a, p)
        if r is not None:
            self.assertEqual((r * r) % p, a % p)
        else:
            self.assertFalse(is_quadratic_residue(a, p))

    def test_non_residue_large_prime(self):
        p = 2147483647
        # Find a non-residue deterministically.
        a = 2
        while is_quadratic_residue(a, p):
            a += 1
        self.assertIsNone(modular_sqrt(a, p))

    def test_rejects_p2(self):
        with self.assertRaises(ValueError):
            modular_sqrt(1, 2)

    def test_rejects_small_p(self):
        with self.assertRaises(ValueError):
            modular_sqrt(1, 1)

    def test_reduction_of_a(self):
        # a larger than p should be reduced automatically.
        p = 7
        r = modular_sqrt(2 + p, p)  # 2 mod 7
        self.assertEqual((r * r) % p, 2)


class TestIsQuadraticResidue(unittest.TestCase):
    def test_residue(self):
        self.assertTrue(is_quadratic_residue(2, 7))

    def test_non_residue(self):
        self.assertFalse(is_quadratic_residue(5, 7))

    def test_zero_is_residue(self):
        self.assertTrue(is_quadratic_residue(0, 7))

    def test_rejects_p2(self):
        with self.assertRaises(ValueError):
            is_quadratic_residue(1, 2)

    def test_all_residues_mod_13(self):
        # Complete enumeration for a small prime.
        residues = {i for i in range(13) if is_quadratic_residue(i, 13)}
        expected = {0, 1, 3, 4, 9, 10, 12}
        self.assertEqual(residues, expected)


if __name__ == "__main__":
    unittest.main()
