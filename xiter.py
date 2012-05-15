import multiprocessing
from itertools import tee, islice, dropwhile, takewhile, chain

import unittest

def I(x):
    return x

class xiter:
    def __init__(self, iterable):
        self.next = iter(iterable).next
        
    def __iter__(self):
        return self
    
    def map(self, f, workers = None, task_size = 1):
        return xiter(f(x) for x in self) if not workers \
          else multiprocessing.Pool(workers).imap(f, self, task_size)
        
    def reduce(self, f, **kwargs):
        return reduce(f, self, **kwargs)
    
    def filter(self, p):
        return xiter(x for x in self if p(x))
        
    def sum(self):
        return sum(self)
        
    def product(self):
        return self.reduce(lambda x, y: x * y)
        
    def all(self, p = I):
        return all(p(x) for x in self)
    
    def any(self, p = I):
        return any(p(x) for x in self)
        
    def none(self, p = I):
        return all(not p(x) for x in self)
        
    def count(self, p = I):
        return len(x for x in self if p(x))
        
    def drop(self, amount):
        return xiter(islice(self, amount, None))
        
    def slice(self, *args, **kwargs):
        return xiter(islice(self, *args, **kwargs))
    
    def dropwhile(self, p = I):
        return xiter(dropwhile(p, self))
        
    def takewhile(self, p = I):
        return xiter(takewhile(p, self))
    
    def tee(self, amount = 2):
        return map(xiter, tee(self, amount))
    
    def find(self, p = I):
        for x in self:
            if p(x): return x

    def findindex(self, p = I):
        for i, x in enumerate(self):
            if p(x): return i

    def max(self, key = I):
        return max(self, key = key)
    
    def min(self, key = I):
        return min(self, key = key)
    
    def enumerate(self):
        return xiter(enumerate(self))
    
    def fork(self, workers = None, task_size = 1, unordered = False):
        pool = multiprocessing.Pool(workers)
        
        return xiter(pool.imap_unordered(I, self, task_size))
    
    def buffer(self, amount = 0):
        if amount == 0:
            return xiter(list(self))
        
        buffered = list(self.slice(0, amount))
        return xiter(chain(buffered, self))


# =============================================================================
# UNIT TEST (well, kinda. I tried. My brain refused):
# =============================================================================

class _xiter_test(unittest.TestCase):

    def setUp(self):
        self.base = xrange(100)
        self.xi   = xiter(xrange(len(self.base)))

    def test_map(self):
        self.verifyl(
            self.xi.map(lambda x: x * 2),
            (2 * x for x in self.base)
        )
    
    def test_reduce(self):
        self.verifyv(
            self.xi.reduce(lambda x, y: x * y + x + y),
            reduce(lambda x, y: x * y + x + y, self.base)
        )
        
    def test_filter(self):
        self.verifyl(
            self.xi.filter(lambda x: x % 2 == 0),
            (x for x in self.base if x % 2 == 0)
        )
    
    def verifyl(self, result, expected):
        return self.assertEqual(list(result), list(expected))
            
    def verifyv(self, result, expected):
        return self.assertEqual(result, expected)
        
if __name__ == '__main__':
    unittest.main()
