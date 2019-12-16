import copy

def factor(v, x, y):
    index = ((x+1)//(y+1)) % 4
    return v[index]

def doit(imp, v):
    impn = []
    for y in range(0, len(imp)):
        row = 0
        for x in range(y, len(imp)):
            f = factor(v, x, y)
            row += f * imp[x]
        row = abs(row)
        row %= 10
        impn.append(row)
    return impn

def part1(text):
    imp = [int(i) for i in text]
    v = [0, 1, 0, -1]
    print(imp[0:8])
    for i in range(0,100):
        imp = doit(imp, v)
        print(imp[0:8])


def doitmore(work):
    work2 = []
    d = 0
    for i in work:
        d += i
        d %= 10
        work2.append(d)
    return work2

def main():
    filename = 'day16_input.txt'
    with open(filename, 'r') as f:
        text = f.read().strip()
    #text = '03036732577212944063491565474664' #84462026
    #part1(text)

    skip = int(text[0:7])
    print(skip)
    shitload = text * 10000
    work = [int(i) for i in reversed(shitload[skip:])]
    for _ in range(0,100):
        work = doitmore(work)
    for x in reversed(work[-8:]):
        print(x, end = '')
    print()

if __name__ == "__main__":
    main()
