import re

'''
15 KTJDG, 12 BHXH => 5 XCVML
'''

def parse_ingrediense(text):
    (d, s) = text.split(' ')
    return (int(d), s)

def parse_recepies(text):
    d = {}
    for line in text.splitlines():
        line = line.replace(' => ', ':')
        line = line.replace(', ', ':')
        groups = [parse_ingrediense(s) for s in line.split(':')]
        d[groups[-1][1]] = groups
    return d

class factory():
    def __init__(self, product, require, factories):
        self.product = product
        self.require = require
        self.factories = factories
        self.orders = {}
        self.total_orders = 0
        self.ore_need = 0

    def request(self, amount, customer):
        change = 0
        if customer in self.orders.keys():
            change = amount - self.orders[customer]
            self.orders[customer] = amount
        else:
            change = amount
            self.orders[customer] = amount
        self.total_orders += change
        self.update_orders()

    def update_orders(self):
        yeald = self.product[0]
        times = self.total_orders // yeald + (self.total_orders % yeald > 0)
        self.ore_need = 0
        for req in self.require:
            if req[1] == 'ORE':
                self.ore_need += times * req[0]
            else:
                self.factories[req[1]].request(times * req[0], self.product[1])

    def get_ore_needed(self):
        return self.ore_need

def main():
    filename = 'day14_input.txt'
    with open(filename, 'r') as f:
        text = f.read()

    factories = {}
    recepies = parse_recepies(text)
    for recep in recepies:
        factories[recep] = factory(recepies[recep][-1], recepies[recep][0:-1], factories)
    factories['FUEL'].request(1, 'TOMTEN')
    total_ore = 0
    for fact in factories.values():
        total_ore += fact.get_ore_needed()
    print(total_ore)


if __name__ == "__main__":
    main()
