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

def main():
    filename = 'day16_input.txt'
    with open(filename, 'r') as f:
        text = f.read().strip()

    imp = [int(i) for i in text] #'80871224585914546619083218645595']
    v = [0, 1, 0, -1]
    print(imp[0:8])
    for i in range(0,100):
        imp = doit(imp, v)
        print(imp[0:8])


if __name__ == "__main__":
    main()
