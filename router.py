import math
import random


class Point:
    """the (x, y) location of a router """

    # x = 0
    # y = 0

    def __init__(self, x=0.0, y=0.0):
        """new point according to the (x,y) location"""
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    # def display(self):
    #     """print the (x, y)"""
    #     print("(" + self.x + ", " + self.y + ")")

    def dist_square(self, p2):
        """return the square of distance between two point"""
        return (self.x - p2.x)**2 + (self.y - p2.y)**2

    def dist(self, p2):
        """return the distance between two point"""
        return math.sqrt(self.dist_square(p2))


class Router:
    """"""
    # domain_len = 0
    # location = Point()
    # value = -1
    # probs = []

    def __init__(self, l=5, p=Point()):
        self.location = p
        self.domain_len = l
        self.probs = [1.0/self.domain_len] * self.domain_len
        self.curr = random.randint(0, l-1)
        self.select = self.get_next_val()
        self.is_satisfied = False

    def __str__(self):
        return "location: " + str(self.location) + ", " + \
                "domain_len: " + str(self.domain_len) + ", " + \
                "probs: " + str(self.probs) + ", " + \
                "curr: " + str(self.curr) + ", " + \
                "select: " + str(self.select)

    def square_check(self, r, critical_sq_dist):
        """return true means satisfied constraint"""
        if self.curr == r.curr and self.location.dist_square(r.location) < critical_sq_dist:
            return False
        return True

    def check(self, r, critical_dist):
        if self.select == r.curr and self.location.dist(r.location) < critical_dist:
            return False
        return True

    def get_next_val(self):
        # print("self.probs = ", self.probs)
        sum_probs = 0
        x = random.random()
        # print("x = ", x)
        val = 0
        for prob in self.probs:
            sum_probs = sum_probs + prob
            # print("sum_probs = ", sum_probs, "val = ", val)
            if x <= sum_probs:
                return val
            val = val + 1
        return self.domain_len - 1

    def update_probs_succeed(self):
        self.probs = [0.0] * self.domain_len
        self.probs[self.select] = 1.0

    def get_location(self):
        return int(self.location.x), int(self.location.y)

    def set_location(self, pos):
        self.location.x, self.location.y = pos

    def update_probs_fail(self, a, b):
        select_p = self.probs[self.select]
        self.probs = [(1-b) * p + b / (self.domain_len - 1 + a/b) for p in self.probs]
        self.probs[self.select] = (1 - b) * select_p + a / (self.domain_len - 1 + a/b)

    def update_probs(self, a, b, is_succeed):
        if is_succeed:
            self.update_probs_succeed()
        else:
            self.update_probs_fail(a, b)
