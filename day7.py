from amplifier import amplifier
import itertools

def main():
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
        while done != 99 or index != 0:
            (done, value) = amps[index].run(value)
            index = (index + 1) % 5

        if max_signal < value:
            max_signal = value
    print(max_signal)

#17790
#19384820

if __name__ == "__main__":
    main()
