
def fuel(mass, part2 = False):
    res = max(int(mass/3) - 2, 0)

    if res == 0:
        return 0
    
    if part2:
        return res + fuel(res, True)
    return res

def main():
    filename = 'day1_input.txt'
    total_fuel = 0
    with open(filename, 'r') as f:
        for line in f:
            total_fuel += fuel(int(line))
    print(total_fuel)

    total_fuel = 0
    with open(filename, 'r') as f:
        for line in f:
            total_fuel += fuel(int(line), True)
    print(total_fuel)

#3406527
#5106932

if __name__ == "__main__":
    main()
