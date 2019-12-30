#
from collections import defaultdict
import itertools
from intcomputer import intcomputer
from amplifier import amplifier


calc = {1: (lambda p, v: do_add(p, v)),
        2: (lambda p, v: do_mult(p, v)),
        3: (lambda p, v: do_read(p, v)),
        4: (lambda p, v: do_write(p, v)),
        5: (lambda p, v: do_jit(p, v)),
        6: (lambda p, v: do_jif(p, v)),
        7: (lambda p, v: do_lt(p, v)),
        8: (lambda p, v: do_eq(p, v))}

def get_value(p, v, n):
    mode = int((v[p] % (10**(n+2)) / (10**(n+1))))
    if mode:
        return int(v[p + n])
    return int(v[v[p + n]])

def do_add(p, v):
    v[v[p + 3]] = get_value(p, v, 1) + get_value(p, v, 2)
    return p + 4

def do_mult(p, v):
    v[v[p + 3]] = get_value(p, v, 1) * get_value(p, v, 2)
    return p + 4

def do_read(p, v):
    v[v[p + 1]] = input('Enter number: ')
    return p + 2

def do_write(p, v):
    print(get_value(p, v, 1))
    return p + 2

def do_jit(p, v):
    if get_value(p, v, 1):
        return get_value(p, v, 2)
    return p + 3

def do_jif(p, v):
    if not get_value(p, v, 1):
        return get_value(p, v, 2)
    return p + 3

def do_lt(p, v):
    v[v[p + 3]] = 1 if get_value(p, v, 1) < get_value(p, v, 2) else 0
    return p + 4

def do_eq(p, v):
    v[v[p + 3]] = 1 if get_value(p, v, 1) == get_value(p, v, 2) else 0
    return p + 4

def intcomp(vector):
    pos = 0
    while vector[pos] % 100 != 99:
        pos = calc[vector[pos] % 100](pos, vector)
    return vector

def run_int_comp(vector, noun, verb):
    vector[1] = noun
    vector[2] = verb
    return intcomp(vector)[0]

def day2():
    filename = 'day2_input.txt'
    with open(filename, 'r') as f:
        text = f.read()
    vector = [int(numeric_string) for numeric_string in text.split(",")]
    target = 19690720
    for noun in range(0, 99):
        for verb in range(0, 99):
          if run_int_comp(vector.copy(), noun, verb) == target:
              print(100 * noun + verb)
              return

def parse_cable(line):
    return [[path[0], int(path[1:])] for path in line.split(",")]

def mark(matrix, x, y, min_dist, length, do_mark):
    if matrix[x][y]:
        dist = matrix[x][y] + length
        if not min_dist or min_dist > dist:
            return dist
    elif do_mark:
        matrix[x][y] = length
    return min_dist

def plot_cable(pos, matrix, cable, min_dist, length, do_mark):
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
        min_dist = mark(matrix, pos[0], pos[1], min_dist, length, do_mark)
    return plot_cable(pos, matrix, cable[1:], min_dist, length, do_mark)

def day3():
    filename = 'day3_input.txt'
    with open(filename, 'r') as f:
        cable1 = parse_cable(f.readline())
        cable2 = parse_cable(f.readline())
    #cable1 = parse_cable('R75,D30,R83,U83,L12,D49,R71,U7,L72')
    #cable2 = parse_cable('U62,R66,U55,R34,D71,R55,D58,R83')
    #cable1 = parse_cable('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51')
    #cable2 = parse_cable('U98,R91,D20,R16,D67,R40,U7,R15,U6,R7')
    matrix = defaultdict(lambda: defaultdict(int))
    plot_cable([0,0], matrix, cable1, 0, 0, True)
    print(plot_cable([0,0], matrix, cable2, 0, 0, False))

# 7020523
#  | fill with same

def next_password(password):
    password = password + 1
    prev = int(password % 10)
    found_recuring = False
    for i in range(1, 6):
        current = int((password % (10 ** (i + 1))) / (10 ** i))
        if prev <= current:
            found_recuring = True
        if prev < current:
            keep = int(password / (10 ** (i + 1)))
            password = int(str(keep) + str(current)*(i + 1))
        prev = current
    if (found_recuring):
        return password
    return next_password(password)

def has_pair(password):
    prev = int(password % 10)
    found_recuring = 0
    for i in range(1, 6):
        current = int((password % (10 ** (i + 1))) / (10 ** i))
        if prev == current:
            found_recuring = found_recuring + 1
        elif found_recuring == 1:
            return True
        else:
            found_recuring = 0
            prev = current
    return found_recuring == 1

def day4():
    start = 178416
    stop = 676461
    count = 0
    while(start < stop):
        start = next_password(start)
        if(has_pair(start)):
    #        print(start)
            count = count + 1
    print(count)
    '''print(has_pair(112233))
    print(has_pair(122233))
    print(has_pair(122335))
    print(has_pair(122344))
    print(has_pair(123456))
    print(has_pair(113456))
    print(has_pair(122456))
    print(has_pair(123356))
    print(has_pair(123446))
    print(has_pair(123455))'''


def day5():
    filename = 'day5_input.txt'
    with open(filename, 'r') as f:
        text = f.read()
    #text = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'
    vector = [int(numeric_string) for numeric_string in text.split(",")]
    print(intcomp(vector)[0])

def day5_new():
    nr = input('Enter number: ')
    comp_input = [nr]
    filename = 'day5_input.txt'
    with open(filename, 'r') as f:
        text = f.read()
    #text = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'
    program = [int(numeric_string) for numeric_string in text.split(",")]
    computer = intcomputer(program, comp_input)
    code = False
    while not code:
        (code, res) = computer.run()
        print(res)  

class node():
    def __init__(self):
        self.parent = None
        self.dist = 0

def parse_tree(text):
    nodes = defaultdict(node)
    for line in text.splitlines():
        pair = [nodes[name] for name in line.split(')')]
        pair[1].parent = pair[0]
    return nodes

def calc_orbits(nodes):
    orbits = 0
    for _, node in nodes.items():
        node = node.parent
        while node:
            node = node.parent
            orbits = orbits + 1
    return orbits

def mark_distance(nodes):
    node = nodes['YOU'].parent
    dist = 0
    while node:
        node.dist = dist
        dist = dist + 1
        node = node.parent

def calc_dist(nodes):
    node = nodes['SAN'].parent
    dist = 0
    while not node.dist:
        dist = dist + 1
        node = node.parent
    return dist + node.dist

def day6():
    filename = 'day6_input.txt'
    with open(filename, 'r') as f:
        text = f.read()
    #text = 'B)C'
    tree = parse_tree(text)
    print(calc_orbits(tree))
    mark_distance(tree)
    print(calc_dist(tree))

def day7():
    filename = 'day7_input.txt'
    with open(filename, 'r') as f:
        text = f.read()
    program = [int(numeric_string) for numeric_string in text.split(",")]
    max_signal = 0
    for seq in itertools.permutations([0,1,2,3,4], 5):
        (_, r1) = amplifier(seq[0], program).run(0)
        (_, r2) = amplifier(seq[1], program).run(r1)
        (_, r3) = amplifier(seq[2], program).run(r2)
        (_, r4) = amplifier(seq[3], program).run(r3)
        (_, r5) = amplifier(seq[4], program).run(r4)
        if max_signal < r5:
            max_signal = r5
    print(max_signal)

    max_signal = 0
    for seq in itertools.permutations([5,6,7,8,9], 5):
        amps = [amplifier(seq[0], program),
                amplifier(seq[1], program),
                amplifier(seq[2], program),
                amplifier(seq[3], program),
                amplifier(seq[4], program)]
        done = False
        index =  0
        value = 0
        while not done or index != 0:
            (done, value) = amps[index].run(value)
            index = (index + 1) % 5

        if max_signal < value:
            max_signal = value
    print(max_signal)

def day8():
    filename = 'day8_input.txt'
    with open(filename, 'r') as f:
        image = f.read()
    width = 25
    hight = 6
    layers =  list(map(''.join, zip(*[iter(image)]*width*hight)))
    count_digits =  [[layer.count('0'), layer.count('1') * layer.count('2')] for layer in layers]
    min_value = min(count_digits, key = lambda x : x[0])
    print(min_value)
    result = ''
    for i in range(0, len(layers[0])):
        layer = 0
        while layers[layer][i] == '2':
            layer = layer + 1
        result = result + layers[layer][i]
    for line in list(map(''.join, zip(*[iter(result)]*width))):
        print(line.replace('0', ' ').replace('1', '*'))
    
def day9():
    filename = 'day9_input.txt'
    with open(filename, 'r') as f:
        text = f.read()
    #text = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
    comp_input = [2]
    program = [int(numeric_string) for numeric_string in text.split(",")]
    computer = intcomputer(program, comp_input)
    code = False
    while not code:
        (code, res) = computer.run()
        if not code:
            print(res)
    #print(computer.program)

def main():
    day9()

if __name__ == "__main__":
    main()