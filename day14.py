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
        self.deliveries = {}
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

    def deliver_to(self, amount, product):
        self.deliveries[product] = amount
        if len(self.deliveries) == len(self.require):
            self.make_deliveries()

    def get_result(self, delivered, yeald, req, res, sour):
        a = delivered * yeald
        b = req
        amount = (a // b) + (a % b > 0)
        #print('%i of %s gives %i of %s' % (delivered, sour, amount, res))
        return amount

    def print_amount(self):
        result = min([self.get_result(self.deliveries[r[1]], self.product[0], r[0], self.product[1], r[1]) for r in self.require])
        print('Produced fuel: %i' % result)

    def make_deliveries(self):
        if self.product[1] == 'FUEL':
            return self.print_amount()
        result = min([self.get_result(self.deliveries[r[1]], self.product[0], r[0], self.product[1], r[1]) for r in self.require])
        control = 0
        for order in self.orders:
            fact = self.factories[order]
            share = round(result * self.orders[order] / self.total_orders)
            control += share
            fact.deliver_to(share, self.product[1])
        #print('Control: %i, had: %i' % (control, result))

def main():
    filename = 'day14_input.txt'
    with open(filename, 'r') as f:
        text = f.read()

    text = '''157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT'''
    factories = {}
    recepies = parse_recepies(text)
    for recep in recepies:
        factories[recep] = factory(recepies[recep][-1], recepies[recep][0:-1], factories)
    factories['FUEL'].request(1, 'TOMTEN')
    total_ore = 0
    ore_factories = []
    for fact in factories.values():
        if fact.get_ore_needed():
            ore_factories.append(fact)
        total_ore += fact.get_ore_needed()
    print('Total ore needed for one fuel: %i' % total_ore)

    mined_ore = 1000000000000

    control = 0
    for fact in ore_factories:
        share = round(mined_ore * fact.get_ore_needed() / total_ore)
        control += share
        fact.deliver_to(share, 'ORE')
    #print('Control: %i, had: %i' % (control, mined_ore))

if __name__ == "__main__":
    main()
