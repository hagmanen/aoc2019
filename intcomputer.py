from collections import defaultdict

class intcomputer():
    def __init__(self, program, input):
        self.program = defaultdict(int)
        for k, v in enumerate(program):
            self.program[k] = v
        self.pointer = 0
        self.input = input
        self.output = 0
        self.exit = 0
        self.rel_offset = 0
        self.calc = {1: self.do_add,
                     2: self.do_mult,
                     3: self.do_read,
                     4: self.do_write,
                     5: self.do_jit,
                     6: self.do_jif,
                     7: self.do_lt,
                     8: self.do_eq,
                     9: self.do_rel_set,
                     99: self.do_exit}

    def read_memory(self, address):
        return self.program[address]

    def write_memory(self, address, value):
        self.program[address] = value

    def get_mode(self, offset):
        mode = int((self.read_memory(self.pointer) % (10**(offset+2)) / (10**(offset+1))))
        return mode

    def get_address(self, offset):
        address = self.read_memory(self.pointer + offset)
        if self.get_mode(offset) == 2:
            address = address + self.rel_offset
        return address

    def get_value(self, offset):
        mode = self.get_mode(offset)
        if mode == 1:
            return self.read_memory(self.pointer + offset)
        return self.read_memory(self.get_address(offset))

    def do_add(self):
        self.write_memory(self.get_address(3), self.get_value(1) + self.get_value(2))
        self.pointer = self.pointer + 4

    def do_mult(self):
        self.write_memory(self.get_address(3), self.get_value(1) * self.get_value(2))
        self.pointer = self.pointer + 4

    def do_read(self):
        self.write_memory(self.get_address(1), self.input.pop(0))
        self.pointer = self.pointer + 2

    def do_write(self):
        self.output = self.get_value(1)
        self.exit = 1
        self.pointer = self.pointer + 2

    def do_jit(self):
        if self.get_value(1):
            self.pointer = self.get_value(2)
        else:
            self.pointer = self.pointer + 3

    def do_jif(self):
        if not self.get_value(1):
            self.pointer = self.get_value(2)
        else:
            self.pointer = self.pointer + 3

    def do_lt(self):
        self.write_memory(self.get_address(3), 1 if self.get_value(1) < self.get_value(2) else 0)
        self.pointer = self.pointer + 4

    def do_eq(self):
        self.write_memory(self.get_address(3), 1 if self.get_value(1) == self.get_value(2) else 0)
        self.pointer = self.pointer + 4

    def do_rel_set(self):
        inc_rel = self.get_value(1)
        self.rel_offset = self.rel_offset + inc_rel
        self.pointer = self.pointer + 2

    def do_exit(self):
        self.exit = 99
        self.pointer = self.pointer + 1

    def run(self):
        self.exit = 0
        while not self.exit:
            #print('Opcode %i @ %i' % (self.program[self.pointer], self.pointer))
            self.calc[self.program[self.pointer] % 100]()
        return (self.exit == 99, self.output)
