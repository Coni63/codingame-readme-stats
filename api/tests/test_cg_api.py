import unittest

from infrastructure.codingame_api import get_points_from_rank

class TestPointsMethods(unittest.TestCase):

    def test_winner(self):
        N = 5000
        for base in [500, 2000, 5000, 10000]:
            self.assertEqual(get_points_from_rank(1, N, base=base), base)

    def test_last(self):
        N = 5000
        for base in [500, 2000, 5000, 10000]:
            self.assertEqual(get_points_from_rank(N, N, base=base), 1)

    def test_known(self):
        BASE = 2500  # Opti
        self.assertEqual(get_points_from_rank(4098, 6090, base=BASE), 13)
        self.assertEqual(get_points_from_rank(216, 399, base=BASE), 33)
        self.assertEqual(get_points_from_rank(25, 990, base=BASE), 2068)
        self.assertEqual(get_points_from_rank(44, 581, base=BASE), 1401)
        self.assertEqual(get_points_from_rank(60, 358, base=BASE), 521)

        BASE = 5000 # battle bot
        self.assertEqual(get_points_from_rank(420, 2662, base=BASE), 1308)
        self.assertEqual(get_points_from_rank(543, 6260, base=BASE), 2392)
        self.assertEqual(get_points_from_rank(1754, 2815, base=BASE), 25)
        self.assertEqual(get_points_from_rank(843, 170320, base=BASE), 4794)
        self.assertEqual(get_points_from_rank(118, 267, base=BASE), 84)

    def test_fail(self):
        with self.assertRaises(ValueError):
            get_points_from_rank(-2, 5000, base=100)

        with self.assertRaises(ValueError):
            get_points_from_rank(750, 500, base=100)

        with self.assertRaises(ValueError):
            get_points_from_rank(500, 5000, base=0)

if __name__ == '__main__':
    unittest.main()