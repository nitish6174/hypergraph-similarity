from collections import deque
from operator import itemgetter


_getitem0 = itemgetter(0)

def hamming_distance(x, y):
    return bin(x ^ y).count('1')


class BKTree(object):
    def __init__(self):
        self.tree = None

    def add(self, item):
        node = self.tree
        if node is None:
            self.tree = (item, {})
            return

        while True:
            parent, children = node
            distance = hamming_distance(item, parent)
            node = children.get(distance)
            if node is None:
                children[distance] = (item, {})
                break

    def find(self, item, n):
        if self.tree is None:
            return []

        candidates = deque([self.tree])
        found = []

        _candidates_popleft = candidates.popleft
        _candidates_extend = candidates.extend
        _found_append = found.append

        while candidates:
            candidate, children = _candidates_popleft()
            distance = hamming_distance(candidate, item)
            if distance <= n:
                _found_append((distance, candidate))

            if children:
                lower = distance - n
                upper = distance + n
                _candidates_extend(c for d, c in children.items() if lower <= d <= upper)

        found.sort(key=_getitem0)
        return found

    def __iter__(self):
        if self.tree is None:
            return

        candidates = deque([self.tree])
        _candidates_popleft = candidates.popleft
        _candidates_extend = candidates.extend

        while candidates:
            candidate, children = _candidates_popleft()
            yield candidate
            _candidates_extend(children.values())

