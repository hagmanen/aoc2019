
def next_password(password):
    password = password + 1
    prev = int(password % 10)
    found_recuring = False
    for i in range(1, 6):
        current = int((password % (10 ** (i + 1))) / (10 ** i))
        if prev <= current:
            found_recuring = True
        if prev < current:
            keep = int(password / (10 ** (i + 1)))
            password = int(str(keep) + str(current)*(i + 1))
        prev = current
    if (found_recuring):
        return password
    return next_password(password)

def has_pair(password):
    prev = int(password % 10)
    found_recuring = 0
    for i in range(1, 6):
        current = int((password % (10 ** (i + 1))) / (10 ** i))
        if prev == current:
            found_recuring = found_recuring + 1
        elif found_recuring == 1:
            return True
        else:
            found_recuring = 0
            prev = current
    return found_recuring == 1

def main():
    start = 178416
    stop = 676461
    count = 0
    while(start < stop):
        start = next_password(start)
        if(has_pair(start)):
            count = count + 1
    print(count)

#1650
#1129

if __name__ == "__main__":
    main()
