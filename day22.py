import re

def op_combine(x, y):
    (a, b) = x
    (c, d) = y
    return (a*c, b*c+d)

def main():
    filename = 'day22_input.txt'
    with open(filename, 'r') as f:
        text = f.read()
    op = (1, 0)
    for line in text.splitlines():
        if line == 'deal into new stack':
            op = op_combine(op, (-1, -1))
        elif m := re.match(r'cut (-?\d*)', line):
            n = int(m.group(1))
            op = op_combine(op, (1, -n))
        elif m := re.match(r'deal with increment (\d*)', line):
            n = int(m.group(1))
            op = op_combine(op, (n, 0))

    deck_size = 10007
    card = 2019
    op = (op[0] % deck_size, op[1] % deck_size)
    pos = (op[0] * card + op[1]) % deck_size
    print(pos)

if __name__ == "__main__":
    main()
