import re

def read_instructions(text, deck_size):
    shuffle = []
    for line in text.splitlines():
        if line == 'deal into new stack':
            shuffle.append(lambda card: deck_size - card - 1)
        elif m := re.match(r'cut (-?\d*)', line):
            cut = int(m.group(1))
            if cut < 0:
                cut += deck_size
            shuffle.append(lambda card, cut=cut: (card + deck_size - cut) if card < cut else (card - cut))
        elif m := re.match(r'deal with increment (\d*)', line):
            deal = int(m.group(1))
            shuffle.append(lambda card, deal=deal: (card * deal) % deck_size)

    return shuffle

def do_shuffle(card, shuffle):
    for f in shuffle:
        card = f(card)
    return card


def main():
    filename = 'day22_input.txt'
    with open(filename, 'r') as f:
        text = f.read()
    
    deck_size = 10007
    shuffle = read_instructions(text, deck_size)

    card = 2019
    print(do_shuffle(card, shuffle))

    deck_size = 119315717514047
    shuffle = read_instructions(text, deck_size)

    card = 2020
    tim = 101741582076661
    #i = 1
    #card = do_shuffle(card, shuffle)
    #print('One shuffle')
    #while card != 2020:
    #    card = do_shuffle(card, shuffle)
    #    i += 1
    #print('Period = %i' % i)
    #tim %= i
    for i in range(0, tim):
        card = do_shuffle(card, shuffle)
        print(card)
    print(card)

if __name__ == "__main__":
    main()
