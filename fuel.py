#
from collections import defaultdict
import itertools
from intcomputer import intcomputer
from amplifier import amplifier

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