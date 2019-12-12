import math
import itertools

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

def main():
    filename = 'day10_input.txt'
    assdroids = []
    with open(filename, 'r') as f:
        y = 0
        for line in f:
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

if __name__ == "__main__":
    main()