import unittest
from router import Point, Router

p = Point(1, 3.0)
p2 = Point(2, 3.0)
r = Router(8, p)
r.probs = [0.05, 0.05, 0.1, 0.1, 0.1, 0.1, 0.2, 0.3]
# a = 0.1
# b = 0.9
#
# for _ in range(50):
#     r.update_probs(a, b, False)
#     r.select = r.get_next_val()
#     print(r.select)
#     print(r.probs)
#     print(sum(r.probs))
#     print()
# count = [0] * 8
# cases = 10000
# for _ in range(cases):
#     x = r.get_next_val()
#     count[x] = count[x] + 1
# print(r.probs)
# print([c / cases for c in count])
# r.get_next_val()
# r.get_next_val()
# r.get_next_val()
# r.get_next_val()
# r.get_next_val()

# print(p)
# x = [0, 0, 0, 0, 0, 0]
# for _ in range(900):
#     r = Router(6, p)
#     x[r.curr] = x[r.curr] + 1
#     print(r)
# print(x)
# r1 = Router(6, p)
# r2 = Router(6, p2)
# r1.curr = 1
# r2.curr = 2
# print(r1.square_check(r2, 0.9))
# print(r1.square_check(r2, 1.0))
# print(r1.square_check(r2, 1.01))
#
# r2.curr = 1
# print(r1.square_check(r2, 0.9))
# print(r1.square_check(r2, 1.0))
# print(r1.square_check(r2, 1.01))


class TestPoint(unittest.TestCase):
    def test_init(self):
        p = Point(1.1, 2.0)
        self.assertEqual(p.x, 1.1)
        self.assertEqual(p.y, 2.0)
        self.assertTrue(isinstance(p, Point))

    def test_square_dist(self):
        p = Point(1.1, 2.0)
        p2 = Point(0.2, -1.1)
        self.assertEqual(p.dist_square(p2), 0.9**2 + 3.1**2)
        p = Point(-1.1, -2.0)
        p2 = Point(-0.2, 1.1)
        self.assertEqual(p.dist_square(p2), 0.9 ** 2 + 3.1 ** 2)

