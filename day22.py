import re

def op_combine(x, y):
    (a, b) = x
    (c, d) = y
    return (a*c, b*c+d)

def part1(op):
    deck_size = 10007
    card = 2019
    op = (op[0] % deck_size, op[1] % deck_size)
    pos = (op[0] * card + op[1]) % deck_size
    print(pos)

def part2():
    m = 119315717514047
    n = 101741582076661
    pos = 2020
    shuffles = { 'deal with increment ': lambda x,m,a,b: (a*x %m, b*x %m),
            'deal into new stack': lambda _,m,a,b: (-a %m, (m-1-b)%m),
            'cut ': lambda x,m,a,b: (a, (b-x)%m) }
    a,b = 1,0
    with open('day22_input.txt') as f:
        for s in f.read().strip().split('\n'):
            for name,fn in shuffles.items():
                if s.startswith(name):
                    arg = int(s[len(name):]) if name[-1] == ' ' else 0
                    a,b = fn(arg, m, a, b)
                    break
    r = (b * pow(1-a, m-2, m)) % m
    print(f"Card at #{pos}: {((pos - r) * pow(a, n*(m-2), m) + r) % m}")

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

    part1(op)
    part2()

#2558
#63967243502561
if __name__ == "__main__":
    main()
