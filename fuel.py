#
from collections import defaultdict
import itertools
from intcomputer import intcomputer
from amplifier import amplifier

def day7():
    filename = 'day7_input.txt'
    with open(filename, 'r') as f:
        text = f.read()
    program = [int(numeric_string) for numeric_string in text.split(",")]
    max_signal = 0
    for seq in itertools.permutations([0,1,2,3,4], 5):
        (_, r1) = amplifier(seq[0], program).run(0)
        (_, r2) = amplifier(seq[1], program).run(r1)
        (_, r3) = amplifier(seq[2], program).run(r2)
        (_, r4) = amplifier(seq[3], program).run(r3)
        (_, r5) = amplifier(seq[4], program).run(r4)
        if max_signal < r5:
            max_signal = r5
    print(max_signal)

    max_signal = 0
    for seq in itertools.permutations([5,6,7,8,9], 5):
        amps = [amplifier(seq[0], program),
                amplifier(seq[1], program),
                amplifier(seq[2], program),
                amplifier(seq[3], program),
                amplifier(seq[4], program)]
        done = False
        index =  0
        value = 0
        while not done or index != 0:
            (done, value) = amps[index].run(value)
            index = (index + 1) % 5

        if max_signal < value:
            max_signal = value
    print(max_signal)

def day8():
    filename = 'day8_input.txt'
    with open(filename, 'r') as f:
        image = f.read()
    width = 25
    hight = 6
    layers =  list(map(''.join, zip(*[iter(image)]*width*hight)))
    count_digits =  [[layer.count('0'), layer.count('1') * layer.count('2')] for layer in layers]
    min_value = min(count_digits, key = lambda x : x[0])
    print(min_value)
    result = ''
    for i in range(0, len(layers[0])):
        layer = 0
        while layers[layer][i] == '2':
            layer = layer + 1
        result = result + layers[layer][i]
    for line in list(map(''.join, zip(*[iter(result)]*width))):
        print(line.replace('0', ' ').replace('1', '*'))
    
def day9():
    filename = 'day9_input.txt'
    with open(filename, 'r') as f:
        text = f.read()
    #text = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
    comp_input = [2]
    program = [int(numeric_string) for numeric_string in text.split(",")]
    computer = intcomputer(program, comp_input)
    code = False
    while not code:
        (code, res) = computer.run()
        if not code:
            print(res)
    #print(computer.program)

def main():
    day9()

if __name__ == "__main__":
    main()