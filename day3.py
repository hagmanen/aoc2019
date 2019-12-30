from collections import defaultdict

def parse_cable(line):
    return [[path[0], int(path[1:])] for path in line.split(",")]

def mark(matrix, x, y, min_dist, length, do_mark, part2):
    if matrix[x][y]:
        if part2:
            dist = matrix[x][y] + length
        else:
            dist = abs(x) + abs(y)
        if not min_dist or min_dist > dist:
            return dist
    elif do_mark:
        matrix[x][y] = length
    return min_dist

def plot_cable(pos, matrix, cable, min_dist, length, do_mark, part2 = False):
    if not len(cable):
        return min_dist
    if cable[0][0] == 'R':
        move = lambda p : [p[0] + 1, p[1]]
    elif cable[0][0] == 'L':
        move = lambda p : [p[0] - 1, p[1]]
    elif cable[0][0] == 'U':
        move = lambda p : [p[0], p[1] + 1]
    elif cable[0][0] == 'D':
        move = lambda p : [p[0], p[1] - 1]
    for _ in range(0, cable[0][1]):
        pos = move(pos)
        length = length + 1
        min_dist = mark(matrix, pos[0], pos[1], min_dist, length, do_mark, part2)
    return plot_cable(pos, matrix, cable[1:], min_dist, length, do_mark, part2)

def main():
    filename = 'day3_input.txt'
    with open(filename, 'r') as f:
        cable1 = parse_cable(f.readline())
        cable2 = parse_cable(f.readline())
    print('Part 1')
    matrix = defaultdict(lambda: defaultdict(int))
    plot_cable([0,0], matrix, cable1, 0, 0, True)
    print(plot_cable([0,0], matrix, cable2, 0, 0, False))
    print('Part 2')
    matrix = defaultdict(lambda: defaultdict(int))
    plot_cable([0,0], matrix, cable1, 0, 0, True)
    print(plot_cable([0,0], matrix, cable2, 0, 0, False, True))

#1285
#14228

if __name__ == "__main__":
    main()
