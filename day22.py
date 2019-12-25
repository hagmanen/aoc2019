import re

def cut_card(card, cut, deck_size):
    card = card - cut
    if card < 0:
        return card + deck_size
    return card

def read_instructions(text, deck_size):
    code = 'card'
    for line in text.splitlines():
        if line == 'deal into new stack':
            code = '%i-%s' % (deck_size - 1, code)
        elif m := re.match(r'cut (-?\d*)', line):
            cut = int(m.group(1))
            if cut < 0:
                cut += deck_size
            code = '(%s+%i)%%%i' % (code, deck_size - cut, deck_size)
        elif m := re.match(r'deal with increment (\d*)', line):
            deal = int(m.group(1))
            code = '((%s)*%i)%%%i' % (code, deal, deck_size)
    print('long long shuffle%i(long long card) {\n  return %s;\n}\n' % (deck_size, code))
    #return eval('lambda card: %s' % code)

def main():
    filename = 'day22_input.txt'
    with open(filename, 'r') as f:
        text = f.read()
    
    #deck_size = 10007
    #shuffle = read_instructions(text, deck_size)

    #card = 2019
    #print(shuffle(card))

    deck_size = 10007
    read_instructions(text, deck_size)

    deck_size = 119315717514047
    read_instructions(text, deck_size)
    return
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
        card = shuffle(card)
        if not i % 1000000:
            print('.', end = '')
    print(card)

if __name__ == "__main__":
    main()
