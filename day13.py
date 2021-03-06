from intcomputer import intcomputer, input_ctrl

def part1(program):
    comp_input =[]
    computer = intcomputer(program, comp_input)
    board = {}
    code = 0
    while code != 99:
        (code, x) = computer.run()
        if code == 99:
            break
        (code, y) = computer.run()
        if code == 99:
            break
        (code, i) = computer.run()
        if code == 99:
            break
        board[(x, y)] = i
    print(sum(1 for value in board.values() if value == 2))

def part2(program):
    program[0] = 2

    comp_input = input_ctrl(0)
    computer = intcomputer(program, comp_input)
    code = 0
    paddle = 0
    ball = 0
    score = 0
    while code != 99:
        (code, x) = computer.run()
        if code == 2:
            continue
        if code == 99:
            break
        (code, y) = computer.run()
        if code == 99:
            break
        (code, i) = computer.run()
        if code == 99:
            break
        if x == -1:
            score = i
            next
        
        if i == 3:
            paddle = x
        if i == 4:
            ball = x

        if ball < paddle:
            comp_input.set_state(-1)
        elif ball > paddle:
            comp_input.set_state(1)
        else:
            comp_input.set_state(0)
    print('Final score: %i' % score)

def main():
    filename = 'day13_input.txt'
    with open(filename, 'r') as f:
        text = f.read()

    program = [int(numeric_string) for numeric_string in text.split(",")]

    part1(program)
    part2(program)

#315
#16171
if __name__ == "__main__":
    main()
