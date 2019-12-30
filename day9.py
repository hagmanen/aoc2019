from intcomputer import intcomputer

def calc_output(program, i):
    computer = intcomputer(program, [i])
    while True:
        (code, res) = computer.run()
        if code == 99:
            return
        if code == 1:
            return res

def main():
    filename = 'day9_input.txt'
    with open(filename, 'r') as f:
        text = f.read()
    program = [int(numeric_string) for numeric_string in text.split(",")]
    print(calc_output(program, 1))
    print(calc_output(program, 2))

#3345854957
#68938

if __name__ == "__main__":
    main()
