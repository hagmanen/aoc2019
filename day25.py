from intcomputer import intcomputer, input_queue
import sys
import itertools

def main():
    filename = 'day25_input.txt'
    with open(filename, 'r') as f:
        text = f.read()

    program = [int(numeric_string) for numeric_string in text.split(",")]
    input_ctrl = []
    computer = intcomputer(program, input_ctrl)
    cmds= ['west', 'south', 'take pointer', 'south', 'take prime number', 'west', 'take coin', 'east', 'north', 'north', 'east',\
           'east', 'south', 'south', 'take space heater', 'south', 'take astrolabe', 'north', 'north', 'north',\
           'north', 'take wreath', 'north', 'west', 'take dehydrated water', 'north', 'east']
    items = ['pointer', 'prime number', 'coin', 'space heater', 'astrolabe', 'wreath', 'dehydrated water']
    for i in itertools.permutations(items, 3):
        cmds.append('drop ' + i[0])
        cmds.append('drop ' + i[1])
        cmds.append('drop ' + i[2])
        cmds.append('south')
        cmds.append('take ' + i[0])
        cmds.append('take ' + i[1])
        cmds.append('take ' + i[2])
    ll = ''
    while True:
        (e, x) = computer.run()
        if e == 99:
            return
        c = chr(x)
        print(c, end = '')
        if x == 10:
            ll = ''
            continue
        ll += c
        if ll == 'Command?':
            if len(cmds):
                line = cmds.pop(0) + '\n'
            else:
                line = sys.stdin.readline()
            input_ctrl.extend([ord(numeric_string) for numeric_string in line])

if __name__ == "__main__":
    main()
