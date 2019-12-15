from intcomputer import intcomputer
import curses


'''
0 is an empty tile. No game object appears in this tile.
1 is a wall tile. Walls are indestructible barriers.
2 is a block tile. Blocks can be broken by the ball.
3 is a horizontal paddle tile. The paddle is indestructible.
4 is a ball tile. The ball moves diagonally and bounces off objects.
'''

def part1(program):
    comp_input =[]
    computer = intcomputer(program, comp_input)
    board = {}
    code = False
    while not code:
        (code, x) = computer.run()
        if code:
            break
        (code, y) = computer.run()
        if code:
            break
        (code, i) = computer.run()
        if code:
            break
        board[(x, y)] = i
    print(sum(1 for value in board.values() if value == 2))
    print('min x: %i' % min([x[0] for x in board.keys()]))
    print('max x: %i' % max([x[0] for x in board.keys()]))
    print('min y: %i' % min([x[1] for x in board.keys()]))
    print('max y: %i' % max([x[1] for x in board.keys()]))

class input_ctrl():
    def __init__(self):
        self.state = 0

    def set_state(self, state):
        self.state = state

    def pop(self, _):
        return self.state

def part2(stdscr):
    filename = 'day13_input.txt'
    with open(filename, 'r') as f:
        text = f.read()

    program = [int(numeric_string) for numeric_string in text.split(",")]

    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    #min x: 0
    #max x: 43
    #min y: 0
    #max y: 22
    program[0] = 2
    symbols = { 0:' ', 1:'#', 2:'X', 3:'=', 4:'O'}

    comp_input = input_ctrl()
    computer = intcomputer(program, comp_input)
    code = False
    stdscr.clear()
    paddle = 0
    ball = 0
    while not code:
        (code, x) = computer.run()
        if code:
            break
        (code, y) = computer.run()
        if code:
            break
        (code, i) = computer.run()
        if code:
            break
        if x == -1:
            stdscr.addstr(0, 0, 'score: %i' % i, curses.color_pair(1))
        else:
            stdscr.addstr(1+y, x, symbols[i], curses.color_pair(1))
        
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
        stdscr.refresh()

    stdscr.getch()


def main():
    filename = 'day13_input.txt'
    with open(filename, 'r') as f:
        text = f.read()

    program = [int(numeric_string) for numeric_string in text.split(",")]

    part1(program)
    curses.wrapper(part2)

if __name__ == "__main__":
    main()
