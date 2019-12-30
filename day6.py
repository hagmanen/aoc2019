from collections import defaultdict

class node():
    def __init__(self):
        self.parent = None
        self.dist = 0

def parse_tree(text):
    nodes = defaultdict(node)
    for line in text.splitlines():
        pair = [nodes[name] for name in line.split(')')]
        pair[1].parent = pair[0]
    return nodes

def calc_orbits(nodes):
    orbits = 0
    for _, node in nodes.items():
        node = node.parent
        while node:
            node = node.parent
            orbits = orbits + 1
    return orbits

def mark_distance(nodes):
    node = nodes['YOU'].parent
    dist = 0
    while node:
        node.dist = dist
        dist = dist + 1
        node = node.parent

def calc_dist(nodes):
    node = nodes['SAN'].parent
    dist = 0
    while not node.dist:
        dist = dist + 1
        node = node.parent
    return dist + node.dist

def main():
    filename = 'day6_input.txt'
    with open(filename, 'r') as f:
        text = f.read()
    #text = 'B)C'
    tree = parse_tree(text)
    print(calc_orbits(tree))
    mark_distance(tree)
    print(calc_dist(tree))

#145250
#274

if __name__ == "__main__":
    main()
