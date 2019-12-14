import operator
import itertools
import re

def velocity_impact(p1, p2):
    if p1 == p2:
        return 0
    if p1 < p2:
        return 1
    return -1

class moon():
    def __init__(self, pos):
        self.pos = pos
        self.vel = (0, 0, 0)

    def interact(self, other):
        velocity_change = tuple(map(velocity_impact, self.pos, other.pos))
        self.vel = tuple(map(operator.add, self.vel, velocity_change))
        other.vel = tuple(map(operator.sub, other.vel, velocity_change))

    def update_pos(self):
        self.pos = tuple(map(operator.add, self.vel, self.pos))

    def print(self, name):
        print('%s pos %s vel %s' % (name, str(self.pos), str(self.vel)))

    def energy(self): 
        return sum([abs(x) for x in self.pos]) * sum([abs(x) for x in self.vel])

def parse_moon(line):
    coords = re.findall(r'[-+]?\d+', line)
    return moon(tuple([int(x) for x in coords]))

def print_moons(moons, iteration):
    id = 0
    print('After %i iterattions' % iteration)
    for moon in moons:
        moon.print('m' + str(id))
        id = id + 1

def main():
    filename = 'day12_input.txt'
    with open(filename, 'r') as f:
        text = f.read()
    moons = []
    for line in text.splitlines():
        moons.append(parse_moon(line))
    
    print_moons(moons, 0)
    for _ in range(1, 1001):
        for pair in itertools.combinations(moons, 2):
            pair[0].interact(pair[1])
        for moon in moons:
            moon.update_pos()
    print_moons(moons, 1000)
    energy = 0
    for moon in moons:
        energy = energy + moon.energy()
    print('Total energy: %i' % energy)

if __name__ == "__main__":
    main()

# HCZRUGAZ