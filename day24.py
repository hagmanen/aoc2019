import copy

def grid_code(grid):
    code = 0
    for y in range(0, 5):
        for x in range(0, 5):
            if grid[(x, y)]:
                code += 1 << ((y*5) + x)
    return code

def neigbours(grid, p):
    return int(grid[(p[0] + 1, p[1])]) + int(grid[(p[0], p[1] + 1)]) + int(grid[(p[0] - 1, p[1])]) + int(grid[(p[0], p[1] - 1)])

def mutate_grid(grid):
    new_grid = copy.copy(grid)
    for y in range(0, 5):
        for x in range(0, 5):
            p = (x, y)
            if grid[p]:
                new_grid[p] = neigbours(grid, p) == 1
            else:
                new_grid[p] = neigbours(grid, p) in [1, 2]
    return new_grid

def main():
    filename = 'day24_input.txt'
    with open(filename, 'r') as f:
        text = f.read()

    grid = {}
    grids = set()

    for y in range(-1, 6):
        for x in range(-1, 6):
            grid[(x, y)] = False

    y = 0
    for line in text.splitlines():
        x = 0
        for c in line:
            grid[(x, y)] = c == '#'
            x += 1
        y += 1

    grids.add(grid_code(grid))

    while True:
        grid = mutate_grid(grid)
        code = grid_code(grid)
        if code in grids:
            for y in range(0, 5):
                for x in range(0, 5):
                    print('#' if grid[(x,y)] else '.', end = '')
                print()
            print("found it: %i" % code)
            return
        grids.add(code)

if __name__ == "__main__":
    main()
