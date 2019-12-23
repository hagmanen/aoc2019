from intcomputer import intcomputer, input_ctrl

def main():
    filename = 'day21_input.txt'
    with open(filename, 'r') as f:
        text = f.read()

    program = [int(numeric_string) for numeric_string in text.split(",")]

    imp_str = 'NOT A J\nNOT C T\nOR T J\nAND D J\nWALK\n'
    comp_input = [ord(c) for c in imp_str]
    computer = intcomputer(program, comp_input)
    m_exit = False
    while not m_exit:
        (m_exit, m_out) = computer.run()
        if m_out < 255:
            print(chr(m_out), end = '')
        else:
            print('WALK Result: %i' % m_out)
    imp_str = 'NOT A J\nNOT B T\nOR T J\nNOT C T\nOR T J\nAND D J\nNOT E T\nNOT T T\nOR H T\nAND T J\nRUN\n'
    comp_input = [ord(c) for c in imp_str]
    computer = intcomputer(program, comp_input)
    m_exit = False
    while not m_exit:
        (m_exit, m_out) = computer.run()
        if m_out < 255:
            print(chr(m_out), end = '')
        else:
            print('RUN Result: %i' % m_out)


if __name__ == "__main__":
    main()
