from intcomputer import intcomputer, input_ctrl

def in_beam(program, x, y):
    comp_input = [x, y]
    computer = intcomputer(program, comp_input)
    (_, m_pull) = computer.run()
    #print('x%iy%i = %s' % (x, y, m_pull == 1))
    return m_pull == 1

def main():
    filename = 'day19_input.txt'
    with open(filename, 'r') as f:
        text = f.read()

    program = [int(numeric_string) for numeric_string in text.split(",")]

    '''
    m_count = 0
    for y in range(0, 50):
        for x in range(0, 50):
            if in_beam(program, x, y):
                m_count += 1
    print(m_count)
    '''

    y = 100
    x = 0
    while True:
        y += 1
        while not in_beam(program, x, y):
            x += 1
        if in_beam(program, x + 99, y - 99):
            print(10000*x + y - 99)
            return

if __name__ == "__main__":
    main()
