import re
import copy

def m_cut(deck, nr):
    if nr < 0:
        nr = nr + len(deck)
    return deck[nr:] + deck[0:nr]

def m_deal(deck, nr):
    new_deck = copy.copy(deck)
    for x in range(0, len(deck)):
        y = (x*nr) % len(deck)
        new_deck[(x*nr) % len(deck)] = deck[x]
    return new_deck

def main():
    filename = 'day22_input.txt'
    with open(filename, 'r') as f:
        text = f.read()

    deck = [x for x in range(0, 10007)]
    #deck = [x for x in range(0, 10)]
    for line in text.splitlines():
        if line == 'deal into new stack':
            deck.reverse()
        elif m := re.match(r'cut (-?\d*)', line):
            deck = m_cut(deck, int(m.group(1)))
        elif m := re.match(r'deal with increment (\d*)', line):
            deck = m_deal(deck, int(m.group(1)))

    #print(deck)
    #'''
    count = 0
    while deck[count] != 2019:
        count += 1
    print(count)
    #'''

if __name__ == "__main__":
    main()
