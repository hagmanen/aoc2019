import math
import itertools
from collections import defaultdict


class assdroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vectors = set()
    
    def add_vector_to(self, other):
        vx = other.x - self.x
        vy = other.y - self.y
        gcd = math.gcd(vx, vy)
        if gcd:
            self.vectors.add((int(vx/gcd), int(vy/gcd)))
            other.vectors.add((-int(vx/gcd), -int(vy/gcd)))

    def visible_assdroids(self):
        return len(self.vectors)

def adjust_angle(x, y):
    f = math.atan2(-x, y)
    if f < 0:
        return 2 * math.pi + f
    return f

def dist(dx, dy):
    return dx * dx + dy * dy

def main():
    filename = 'day10_input.txt'
    assdroids = []
    with open(filename, 'r') as f:
        text = f.read()

    y = 0
    for line in text.splitlines():
        x = 0
        for c in line:
            if c == '#':
                assdroids.append(assdroid(x, y))
            x = x + 1
        y = y + 1
    for a1, a2 in itertools.permutations(assdroids, 2):
        a1.add_vector_to(a2)
    w = max(assdroids, key=lambda a: a.visible_assdroids())
    print('%i %i, see %i' % ( w.x, w.y, w.visible_assdroids()))

    d = defaultdict(lambda : [])
    y = 0
    for line in text.splitlines():
        x = 0
        for c in line:
            if c == '#' and (x != w.x or y != w.y):
                vx = w.x - x
                vy = w.y - y
                gcd = math.gcd(vx, vy)
                vx = int(vx/gcd)
                vy = int(vy/gcd)
                d[(vx, vy)].append((x, y))
                d[(vx, vy)].sort(key = lambda p : dist(p[0] - w.x, p[1] - w.y)) 
            x = x + 1
        y = y + 1
    p = 0
    while d:
        for a in sorted(d, key = lambda b : adjust_angle(*b)):
            p = p + 1
            (nx, ny) = d[a].pop()
            if p == 200:
                print('%i: %i %i score: %i' % (p, nx, ny, 100 * nx + ny))
            if not d[a]:
                del d[a]


if __name__ == "__main__":
    main()