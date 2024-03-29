from django.test import TestCase

from ..func_bonus import *


class Test(TestCase):
    def test_distribute_bonus(self):
        input_data = [
            [50, 50],
            [50, 40],
            [50, 50, 50],
            [50, 50, 40],
            [50, 40, 40],
            [50, 40, 30],
            [50, 50, 50, 50],
            [50, 50, 50, 40],
            [50, 50, 40, 40],
            [50, 40, 40, 40],
            [50, 40, 30, 30],
            [50, 40, 30, 20],
            [50, 40, 40, 30],
            [50, 50, 40, 30],
            [40, 40, 40, 40, 40],
            [50, 40, 40, 40, 40],
            [50, 50, 50, 50, 50, 50],
            [50, 40, 40, 30, 30, 20],
            [50, 45, 40, 35, 30, 25],
            [50 + 0.1 + 0.2, 50 + 0.3, 45],
        ]
        res_data = [
            [1.0, 1.0],
            [2.0, 0.0],
            [1.0, 1.0, 1.0],
            [1.5, 1.5, 0.0],
            [2.0, 0.5, 0.5],
            [2.0, 1.0, 0.0],
            [1.0, 1.0, 1.0, 1.0],
            [4.0 / 3.0, 4.0 / 3.0, 4.0 / 3.0, 0.0],
            [1.5, 1.5, 0.5, 0.5],
            [2.0, 2.0 / 3.0, 2.0 / 3.0, 2.0 / 3.0],
            [2.0, 1.0, 0.5, 0.5],
            [2.0, 1.0, 1.0, 0.0],
            [2.0, 1.0, 1.0, 0.0],
            [1.5, 1.5, 1.0, 0.0],
            [1.0, 1.0, 1.0, 1.0, 1.0],
            [2.0, 0.75, 0.75, 0.75, 0.75],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [2.0, 1.0, 1.0, 1.0, 1.0, 0.0],
            [2.0, 1.0, 1.0, 1.0, 1.0, 0.0],
            [1.5, 1.5, 0.0],
        ]
        for inp, res in zip(input_data, res_data):
            self.assertEqual(distribute_bonus_points(inp), res)
