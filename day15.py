from intcomputer import intcomputer, input_ctrl
from collections import defaultdict

addjustment = {1: (-1, 0), 2: (1, 0), 3: (0, 1), 4: (0, -1)}

def new_pos(pos, direction):
    return (pos[0] + addjustment[direction][0], pos[1] + addjustment[direction][1])

def rev_dir(direction):
    if direction == 1:
        return 2
    if direction == 2:
        return 1
    if direction == 3:
        return 4
    return 3

class Coord():
    def __init__(self, pos):
        self.pos = pos
        self.distance = 0
        self.visited = False
        self.not_explored = [1, 2, 3, 4]
        self.type = 0

    def explore(self, from_dir, distance, type, game_map, ctrl):
        if not self.visited or self.distance > distance:
            self.distance = distance
            self.visited = True

        self.type = type
        if type == 0:
            return
        if type == 2:
            print('Found target after %i steps' % self.distance)

        self.not_explored.remove(from_dir)

        while self.not_explored:
            direction = self.not_explored.pop(0)
            next_pos = new_pos(self.pos, direction)
            next_room = game_map[next_pos]
            if not next_room.visited:
                next_room.explore(rev_dir(direction), distance + 1, ctrl.move(direction), game_map, ctrl)
        ctrl.move(from_dir)

class Ctrl():
    def __init__(self, program):
        self.comp_input = input_ctrl(1)
        self.computer = intcomputer(program, self.comp_input)

    def move(self, direction):
        self.comp_input.set_state(direction)
        (e, r) = self.computer.run()
        return r

class mydefaultdict(defaultdict):
    def __missing__(self, key):
        self[key] = new = self.default_factory(key)
        return new

def main():
    filename = 'day15_input.txt'
    with open(filename, 'r') as f:
        text = f.read()

    program = [int(numeric_string) for numeric_string in text.split(",")]

    ctrl = Ctrl(program)
    pos = (0, 0)
    direction = 1
    game_map = mydefaultdict(Coord)
    while game_map[pos].not_explored:
        direction = game_map[pos].not_explored.pop(0)
        next_pos = new_pos(pos, direction)
        next_room = game_map[next_pos]
        if not next_room.visited:
            next_room.explore(rev_dir(direction), 1, ctrl.move(direction), game_map, ctrl)

    with_oxigen = set()
    without_oxigen = set()
    for coord in game_map:
        if game_map[coord].type == 0:
            continue
        if game_map[coord].type == 1:
            without_oxigen.add(coord)
        else:
            with_oxigen.add(coord)
    steps = 0
    while without_oxigen:
        steps += 1
        filled = set()
        for coord in with_oxigen:
            for direction in range(1,5):
                next_pos = new_pos(coord, direction)
                if next_pos in without_oxigen:
                    filled.add(next_pos)
        for coord in filled:
            without_oxigen.discard(coord)
        with_oxigen = filled
    print('Took %i minutes' % steps)

#222
#394
if __name__ == "__main__":
    main()
