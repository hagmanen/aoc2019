from intcomputer import intcomputer

def calc_output(program, i):
    comp_input = [i]
    computer = intcomputer(program, comp_input)
    while True:
        (e, x) = computer.run()
        if e == 99:
            break
        if e == 1:
            if x != 0:
                return x

def main():
    filename = 'day5_input.txt'
    with open(filename, 'r') as f:
        text = f.read()
    program = [int(numeric_string) for numeric_string in text.split(",")]

    print(calc_output(program, 1))
    print(calc_output(program, 5))

#13087969
#14110739

if __name__ == "__main__":
    main()
