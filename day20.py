import copy

example = '''             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     '''

def get_label(m_map, p):
    ds = [(1,0), (0,1), (-1,0), (0,-1)]
    for d in range(0, len(ds)):
        n = (p[0] + ds[d][0], p[1] + ds[d][1])
        d2 = (d + 2) % 4
        o = (p[0] + ds[d2][0], p[1] + ds[d2][1])
        if not ((n in m_map) and (o in m_map)):
            continue
        if m_map[n] == '.':
            label = m_map[o] + m_map[p] if d in [0, 1] else m_map[p] + m_map[o]
            del m_map[o]
            del m_map[p]
            m_map[n] = 'L'
            return (n, label)
    return None

def find_labels(m_map):
    nodes = {}
    items = [item for item in m_map.items() if item[1] != '.']
    for (p, v) in items:
        label = get_label(m_map, p)
        if label:
            if label[1] in nodes:
                nodes[label[1]].append(label[0])
            else:
                nodes[label[1]] = [label[0]]
    return nodes

def get_neigbour(m_from, m_dir, m_dirs, m_map):
    m_pos = (m_from[0] + m_dir[0], m_from[1] + m_dir[1])
    if not m_pos in m_map:
        return None
    if m_map[m_pos] != '.':
        return (m_pos, 1)
    next_dir = None
    for d in m_dirs:
        next_pos = (m_pos[0] + d[0], m_pos[1] + d[1])
        if next_pos != m_from and next_pos in m_map:
            if next_dir:
                return (m_pos, 1)
            else:
                next_dir = d
    if next_dir:
        n = get_neigbour(m_pos, next_dir, m_dirs, m_map)
        if n:
            return (n[0], n[1] + 1)
    return None

def parse_maze(m_pos, m_map, m_dirs, m_graph):
    m_graph[m_pos] = {}
    for d in m_dirs:
        n = get_neigbour(m_pos, d, m_dirs, m_map)
        if n and n[0] != m_pos:
            if n[0] in m_graph[m_pos]:
                m_graph[m_pos][n[0]] = min(n[1], m_graph[m_pos][n[0]])
            else:
                m_graph[m_pos][n[0]] = n[1]

def find_shortest(m_graph, m_pos, m_target, m_walked, shortest_found, m_visisted, m_level_change, story):
    if m_pos == m_target:
        #print('%s %i' % (story, m_walked))
        return m_walked
    if m_pos[1] < 0:
        return shortest_found
    if (m_pos in m_visisted) and (m_visisted[m_pos] < m_walked):
        return shortest_found
    if shortest_found and shortest_found < m_walked:
        return shortest_found
    if not m_pos[0] in m_graph:
        return shortest_found
    m_visisted[m_pos] = m_walked
    sorter = lambda x, m_level_change=m_level_change: m_level_change[x[0]]
    for m_next in sorted(m_graph[m_pos[0]].items(), key = sorter):
        level = m_pos[1]
        if m_level_change[m_next[0]] + m_level_change[m_pos[0]] == 0:
            level += m_level_change[m_pos[0]]
        sf = find_shortest(m_graph, (m_next[0], level), m_target, m_walked + m_next[1], shortest_found, m_visisted, m_level_change, story + str((m_next[0], level)))
        if not shortest_found or shortest_found > sf:
            shortest_found = sf
    return shortest_found

def main():
    m_filename = 'day20_input.txt'
    with open(m_filename, 'r') as f:
        m_text = f.read()

    #m_text = example
    m_map = {}
    y = 0
    for line in m_text.splitlines():
        x = 0
        for c in line:
            if not c in '# ':
                m_map[(x, y)] = c
            x += 1
        y += 1

    x_edge = [2, x - 3]
    y_edge = [2, y - 3]

    labels = find_labels(m_map)

    m_dirs = [(1,0), (0,1), (-1,0), (0,-1)]
    m_graph = {}
    m_left = set()
    [m_left.update(s) for s in labels.values()]
    while m_left:
        next_node = m_left.pop()
        parse_maze(next_node, m_map, m_dirs, m_graph)
        [m_left.add(n) for n in m_graph[next_node] if not n in m_graph]

    for c in labels.values():
        if len(c) == 2:
            m_graph[c[0]][c[1]] = 1
            m_graph[c[1]][c[0]] = 1

    while True:
        dead_ends = [c for c in m_graph if len(m_graph[c]) == 1 and m_map[c] == '.']
        if not dead_ends:
            break
        for dead_end in dead_ends:
            for neigbour in m_graph[dead_end]:
                del m_graph[neigbour][dead_end]
            del m_graph[dead_end]

    m_level_change = {}
    teleporters = set()
    for coords in labels.values():
        teleporters.update(coords)
    for node in m_graph.keys():
        if node in teleporters:
            if node[0] in x_edge or node[0] in y_edge:
                m_level_change[node] = 0
            else:
                m_level_change[node] = 0
        else:
            m_level_change[node] = 0
    m_level_change[labels['AA'][0]] = 0
    m_level_change[labels['ZZ'][0]] = 0

    to_remove = []
    for (k, v) in m_graph.items():
        if len(v) == 2:
            items = [x for x in v.items()]
            p1 = items[0][0]
            p2 = items[1][0]
            if (p1 in teleporters) or (p2 in teleporters):
                continue
            l = items[0][1] + items[1][1]
            del m_graph[p1][k]
            m_graph[p1][p2] = l
            del m_graph[p2][k]
            m_graph[p2][p1] = l
            to_remove.append(k)

    for p in to_remove:
        del m_graph[p]

    print('Day20 part 1')
    print(find_shortest(m_graph, (labels['AA'][0], 0), (labels['ZZ'][0], 0), 0, None, {}, m_level_change, ''))

    for node in m_graph.keys():
        if node in teleporters:
            if (node[0] in x_edge) or (node[1] in y_edge):
                m_level_change[node] = -1
            else:
                m_level_change[node] = 1
    m_level_change[labels['AA'][0]] = 0
    m_level_change[labels['ZZ'][0]] = 0

    print('Day20 part 2')
    #print('Start %s %s' % (labels['AA'][0], m_graph[labels['AA'][0]]))
    #for x in m_graph.items():
    #    print(x)
    print(find_shortest(m_graph, (labels['AA'][0], 0), (labels['ZZ'][0], 0), 0, 10000, {}, m_level_change, ''))

#578
#6592
if __name__ == "__main__":
    main()
