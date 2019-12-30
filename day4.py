
def next_password(password, part2 = False):
    password = password + 1
    prev = int(password % 10)
    found_recuring = False
    for i in range(1, 6):
        current = (password % (10 ** (i + 1))) // (10 ** i)
        if prev <= current:
            found_recuring = True
        if prev < current:
            keep = password - password % (10 ** (i + 1))
            password = keep + int(str(current)*(i + 1))
        prev = current
    if (found_recuring):
        return password
    return next_password(password)

def has_pair(password, part2 = False):
    prev = int(password % 10)
    found_recuring = 0
    for i in range(1, 6):
        current = int((password % (10 ** (i + 1))) / (10 ** i))
        if prev == current:
            if not part2:
                return True
            found_recuring = found_recuring + 1
        elif found_recuring == 1:
            return True
        else:
            found_recuring = 0
            prev = current
    return found_recuring == 1

def calc_output(part2 = False):
    start = 178416
    stop = 676461
    count = 0
    while(start < stop):
        if(has_pair(start, part2)):
            count = count + 1
        start = next_password(start, part2)
    return count

def main():
    print('Part 1')
    print(calc_output())
    print('Part 2')
    print(calc_output(True))

#1650
#1129

if __name__ == "__main__":
    main()
