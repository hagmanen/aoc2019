from intcomputer import intcomputer

def calc_output(text, noun, verb):
    program = [int(numeric_string) for numeric_string in text.split(",")]
    inputs = []
    program[1] = noun
    program[2] = verb
    computer = intcomputer(program, inputs)

    while True:
        (e, x) = computer.run()
        if e == 99:
            break
    return computer.read_memory(0)

def main():
    filename = 'day2_input.txt'
    with open(filename, 'r') as f:
        text = f.read()

    print(calc_output(text, 12, 2))
    target = 19690720
    for noun in range(0, 99):
        for verb in range(0, 99):
          if calc_output(text, noun, verb) == target:
              print(100 * noun + verb)
              return

#replace position 1 with the value 12 and replace position 2 with the value 2. 
#3101878
#8444

if __name__ == "__main__":
    main()
