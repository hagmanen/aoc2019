import copy

def get_grid(grids, level, added_grids):
    if not level in grids:
        grids[level] = create_grid()
        added_grids.add(level)
    return grids[level]

def neigbours_right(grids, level, x, y, added_grids):
    if x == 4:
        grid = get_grid(grids, level-1, added_grids)
        return int(grid[(3, 2)])
    if x == 1 and y == 2:
        grid = get_grid(grids, level+1, added_grids)
        return sum([int(grid[(0, y)]) for y in range(0,5)])
    return int(grids[level][(x+1, y)])

def neigbours_left(grids, level, x, y, added_grids):
    if x == 0:
        grid = get_grid(grids, level-1, added_grids)
        return int(grid[(1, 2)])
    if x == 3 and y == 2:
        grid = get_grid(grids, level+1, added_grids)
        return sum([int(grid[(4, y)]) for y in range(0,5)])
    return int(grids[level][(x-1, y)])

def neigbours_up(grids, level, x, y, added_grids):
    if y == 0:
        grid = get_grid(grids, level-1, added_grids)
        return int(grid[(2, 1)])
    if y == 3 and x == 2:
        grid = get_grid(grids, level+1, added_grids)
        return sum([int(grid[(x, 4)]) for x in range(0,5)])
    return int(grids[level][(x, y-1)])

def neigbours_down(grids, level, x, y, added_grids):
    if y == 4:
        grid = get_grid(grids, level-1, added_grids)
        return int(grid[(2, 3)])
    if y == 1 and x == 2:
        grid = get_grid(grids, level+1, added_grids)
        li = [int(grid[(x, 0)]) for x in range(0,5)]
        nr = sum(li)
        return nr
    return int(grids[level][(x, y+1)])

def neigbours(grids, level, p, added_grids):
    (x, y) = p
    bug_count = neigbours_right(grids, level, x, y, added_grids)
    bug_count += neigbours_left(grids, level, x, y, added_grids)
    bug_count += neigbours_up(grids, level, x, y, added_grids)
    bug_count += neigbours_down(grids, level, x, y, added_grids)
    return bug_count

def mutate_grid(grids, level, added_grids):
    new_grid = copy.copy(grids[level])
    for y in range(0, 5):
        for x in range(0, 5):
            p = (x, y)
            if p == (2,2):
                continue
            n_count = neigbours(grids, level, p, added_grids)
            if grids[level][p]:
                new_grid[p] = (n_count == 1)
            else:
                new_grid[p] = (n_count == 1 or n_count ==2)
    return new_grid

def grid_empty(grid):
    for b in grid.values():
        if b:
            return False
    return True

def mutate_grids(grids):
    new_grids = {}
    added_grids = set()
    existing_levels = [x for x in grids.keys()]
    for level in existing_levels:
        new_grids[level] = mutate_grid(grids, level, added_grids)
    for level in added_grids:
        new_grids[level] = mutate_grid(grids, level, set())
    existing_levels = [x for x in new_grids.keys()]
    for level in existing_levels:
        if grid_empty(new_grids[level]):
            del new_grids[level]
    return new_grids

def create_grid():
    grid = {}
    for y in range(0,5):
        for x in range(0,5):
            grid[(x, y)] = False
    return grid

def print_grid(grid):
    for y in range(0, 5):
        for x in range(0, 5):
            print('#' if grid[(x,y)] else '.', end = '')
        print()

def main():
    filename = 'day24_input.txt'
    with open(filename, 'r') as f:
        text = f.read()

    grids = set()
    grids = {0: create_grid()}

    y = 0
    for line in text.splitlines():
        x = 0
        for c in line:
            grids[0][(x, y)] = c == '#'
            x += 1
        y += 1

    print('First gen:')
    print_grid(grids[0])
    for _ in range(0, 200):
        grids = mutate_grids(grids)
    bug_count = 0
    for grid in grids.values():
        for bug in grid.values():
            bug_count += int(bug)

    for level in sorted(grids.keys()):
        print('Level %i' % level)
        print_grid(grids[level])
    print(bug_count)

if __name__ == "__main__":
    main()
