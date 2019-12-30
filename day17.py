from intcomputer import intcomputer, input_ctrl

def f_is_intersection(m_scaffold, m_scaffolds):
    (x, y) = m_scaffold
    hits = 0
    if (x-1, y) in m_scaffolds:
        hits += 1
    if (x+1, y) in m_scaffolds:
        hits += 1
    if (x, y-1) in m_scaffolds:
        hits += 1
    if (x, y+1) in m_scaffolds:
        hits += 1
    return hits >= 3

def main():
    m_filename = 'day17_input.txt'
    with open(m_filename, 'r') as f:
        m_text = f.read()

    m_program = [int(numeric_string) for numeric_string in m_text.split(",")]

    m_computer = intcomputer(m_program, [])

    x = 0
    y = 0
    m_scaffolds = set()
    m_intersections = set()
    while True:
        (m_exit, m_res) = m_computer.run()
        if m_exit == 99:
            break
        if m_res == 10:
            y += 1
            x = 0
            continue
        if m_res == ord('#'):
            m_scaffolds.add((x, y))
        elif m_res == ord('.'):
            pass
        elif m_res == ord('^'):
            m_scaffolds.add((x, y))
        elif m_res == ord('v'):
            m_scaffolds.add((x, y))
        elif m_res == ord('<'):
            m_scaffolds.add((x, y))
        elif m_res == ord('>'):
            m_scaffolds.add((x, y))
        x += 1
    for m_scaffold in m_scaffolds:
        if f_is_intersection(m_scaffold, m_scaffolds):
            m_intersections.add(m_scaffold)

    m_sum = 0
    for m_intersection in m_intersections:
        m_sum += m_intersection[0] * m_intersection[1]
    print('Part 1')
    print(m_sum)

    m_input_str = 'A,B,A,C,B,A,B,C,C,B\nL,12,L,12,R,4\nR,10,R,6,R,4,R,4\nR,6,L,12,L,12\nn\n'
    m_input = [ord(c) for c in m_input_str]

    m_program[0] = 2
    m_computer = intcomputer(m_program, m_input)
    while True:
        (m_exit, m_res) = m_computer.run()
        if m_exit == 99:
            break
        elif m_res == 10:
            continue
        elif not str(chr(m_res)).isprintable():
            print('Part 2')
            print('%i' % m_res)

#5724
#732985
if __name__ == "__main__":
    main()
