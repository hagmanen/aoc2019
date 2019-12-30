
def main():
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

#828
#ZLBJF

if __name__ == "__main__":
    main()
