import operator
import itertools
import re
import copy
import math

def velocity_impact(p1, p2):
    if p1 == p2:
        return 0
    if p1 < p2:
        return 1
    return -1

class moon():
    def __init__(self, pos):
        self.pos = pos
        self.vel = tuple([0] * len(pos))

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

    def equal(self, other):
        return self.pos == other.pos and self.vel == other.vel

def parse_moon(line):
    coords = re.findall(r'[-+]?\d+', line)
    return tuple([int(x) for x in coords])

def print_moons(moons, iteration):
    id = 0
    print('After %i iterattions' % iteration)
    for moon in moons:
        moon.print('m' + str(id))
        id = id + 1

def part1(moons):
    combinations = [x for x in itertools.combinations(moons, 2)]
    for _ in range(0, 1000):
        [m1.interact(m2) for m1, m2 in combinations]
        [moon.update_pos() for moon in moons]
            
    print_moons(moons, 1000)
    energy = 0
    for moon in moons:
        energy += moon.energy()
    print('Total energy: %i' % energy)

def get_period(moons):
    combinations = [x for x in itertools.combinations(moons, 2)]
    original_moons = [copy.deepcopy(m) for m in moons]
    diff_moons = [x for x in zip(moons, original_moons)]
    it = 0
    while True:
        [m1.interact(m2) for m1, m2 in combinations]
        [moon.update_pos() for moon in moons]
            
        it = it + 1
        if all(m0.equal(m1) for m0, m1 in diff_moons):
            return it

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

def part2(moonsx, moonsy, moonsz):
    px = get_period(moonsx)
    py = get_period(moonsy)
    pz = get_period(moonsz)

    print(lcm(lcm(px, py), pz))
    

def main():
    filename = 'day12_input.txt'
    with open(filename, 'r') as f:
        text = f.read()
    moons = []
    moonsx = []
    moonsy = []
    moonsz = []
    for line in text.splitlines():
        pos = parse_moon(line)
        moons.append(moon(pos))
        moonsx.append(moon(tuple([pos[0]])))
        moonsy.append(moon(tuple([pos[1]])))
        moonsz.append(moon(tuple([pos[2]])))
    
    part1(moons)

    part2(moonsx, moonsy, moonsz)

if __name__ == "__main__":
    main()
