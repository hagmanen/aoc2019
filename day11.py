'''
First, it will output a value indicating the color to paint the panel the robot is over: 0 means to paint the panel black, and 1 means to paint the panel white.
Second, it will output a value indicating the direction the robot should turn: 0 means it should turn left 90 degrees, and 1 means it should turn right 90 degrees.
'''
import operator
from intcomputer import intcomputer

def turn(dir, cmd):
    if cmd:
        return (dir + 1) % 4
    return (dir + 3) % 4

def marking(val):
    if val:
        return '#'
    return ' '

def main():
    filename = 'day11_input.txt'
    with open(filename, 'r') as f:
        text = f.read()
    #text = ''
    comp_input =[1]
    program = [int(numeric_string) for numeric_string in text.split(",")]
    computer = intcomputer(program, comp_input)
    code = False
    pos = (0, 0)
    direction = 0
    plates = {}
    min_pos = (0, 0)
    max_pos = (0, 0)
    steps = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    while not code:
        (code, res) = computer.run()
        if code:
            break
        plates[pos] = res
        (code, res) = computer.run()
        if code:
            break
        direction = turn(direction, res)
        pos = tuple(map(operator.add, pos, steps[direction]))
        min_pos = tuple(map(min, pos, min_pos))
        max_pos = tuple(map(max, pos, min_pos))
        comp_input.append(plates[pos] if pos in plates else 0)
    print(len(plates))
    for y in range(min_pos[0], max_pos[0] + 2):
        line = ''
        for x in range(min_pos[1], max_pos[1] + 2):
            pos = (y, x)
            line = line + marking(plates[pos] if pos in plates else 0)
        print(line)

if __name__ == "__main__":
    main()

# HCZRUGAZ