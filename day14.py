import re

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

def ore_for(fuel, recepies):
    factories = {}
    for recep in recepies:
        factories[recep] = factory(recepies[recep][-1], recepies[recep][0:-1], factories)
    factories['FUEL'].request(fuel, 'TOMTEN')
    total_ore = 0
    for fact in factories.values():
        total_ore += fact.get_ore_needed()
    return total_ore

def get_next_amount(increase, change, amount):
    if increase:
        return amount + pow(2, change)
    return amount - pow(2, change)

def main():
    filename = 'day14_input.txt'
    with open(filename, 'r') as f:
        text = f.read()

    recepies = parse_recepies(text)

    print('Total ore needed for one fuel: %i' % ore_for(1, recepies))

    increase = True
    amount = 0
    target = 1000000000000
    change = 16
    while True:
        amount = get_next_amount(increase, change, amount)
        ore = ore_for(amount, recepies)
        if ore == target or change < 0:
            print('Got %i fuel' %amount)
            return
        if (increase and ore > target) or (not increase and ore < target):
            increase = not increase
            change -= 1            

if __name__ == "__main__":
    main()
