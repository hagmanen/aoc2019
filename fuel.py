#
from collections import defaultdict
import itertools
from intcomputer import intcomputer

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