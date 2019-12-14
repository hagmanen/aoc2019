import operator
import itertools
import re
import copy

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
        velocity_change = (velocity_impact(self.pos[0], other.pos[0]), velocity_impact(self.pos[1], other.pos[1]), velocity_impact(self.pos[2], other.pos[2]))
        self.vel = (self.vel[0] + velocity_change[0], self.vel[1] + velocity_change[1], self.vel[2] + velocity_change[2])
        other.vel = (other.vel[0] - velocity_change[0], other.vel[1] - velocity_change[1], other.vel[2] - velocity_change[2])

    def update_pos(self):
        self.pos = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1], self.pos[2] + self.vel[2])

    def print(self, name):
        print('%s pos %s vel %s' % (name, str(self.pos), str(self.vel)))

    def energy(self): 
        return sum([abs(x) for x in self.pos]) * sum([abs(x) for x in self.vel])

    def equal(self, other):
        return self.pos == other.pos and self.vel == other.vel

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
    
    original_moons = [copy.deepcopy(m) for m in moons]
    diff_moons = [x for x in zip(moons, original_moons)]
    print_moons(moons, 0)
    it = 0
    combinations = [x for x in itertools.combinations(moons, 2)]
    print(combinations)
    while True:
        [m1.interact(m2) for m1, m2 in combinations]
        [moon.update_pos() for moon in moons]
            
        it = it + 1
        if it == 1000:
            print_moons(original_moons, 0)
            print_moons(moons, it)
            energy = 0
            for moon in moons:
                energy = energy + moon.energy()
            print('Total energy: %i' % energy)
        if not(it % 100000):
            print('.', end = '', flush = True)
        if not(it % 1000000):
            print('')
            print_moons(moons, it)
        if all(m0.equal(m1) for m0, m1 in diff_moons):
            break
    print_moons(moons, it)

if __name__ == "__main__":
    main()
