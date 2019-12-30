from intcomputer import intcomputer, input_queue


def main():
    filename = 'day23_input.txt'
    with open(filename, 'r') as f:
        text = f.read()

    program = [int(numeric_string) for numeric_string in text.split(",")]


    inputs = []
    computers = []
    nat = [0, 0]
    last_nat = [0, 0]
    idle_count = 0
    first_nat = None

    for addr in range(0, 50):
        inputs.append(input_queue())
        inputs[addr].put(addr)
        computers.append(intcomputer(program, inputs[addr]))

    while True:
        for addr in range(0, 50):
            mes = []
            tried_once = False
            while True:
                (e, x) = computers[addr].run()
                if e == 2 and tried_once:
                    idle_count += 1
                    break
                if e == 2:
                    tried_once = True
                    continue
                tried_once = False
                idle_count = 0
                #print('Got %i from %i' % (x, addr))
                mes.append(x)
                if len(mes) == 3:
                    #print('Send (%i,%i) to %i' % (mes[1], mes[2], mes[0]))
                    if mes[0] == 255:
                        if not first_nat:
                            first_nat = mes[1:]
                        nat = mes[1:]
                    else:
                        inputs[mes[0]].put(mes[1])
                        inputs[mes[0]].put(mes[2])
                    mes = []
            if idle_count == 50:
                if last_nat == nat:
                    print('Part 1')
                    print(first_nat)
                    print('Part 2')
                    print(nat)
                    return 
                last_nat = [x for x in nat]
                inputs[0].put(nat[0])
                inputs[0].put(nat[1])

#14834
#10215
if __name__ == "__main__":
    main()
