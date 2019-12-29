import copy

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

def get_map_and_nodes(m_text):
    m_map = {}
    m_keys = {}
    m_entrance = None
    y = 0
    for line in m_text.splitlines():
        x = 0
        for c in line:
            if c != '#':
                m_map[(x, y)] = c
                if c.islower():
                    m_keys[c] = (x, y)
                if c == '@':
                    m_entrance = (x, y)
            x += 1
        y += 1
    return (m_map, m_keys, m_entrance)

def get_graph(m_map, m_entrances):
    m_dirs = [(1,0), (0,1), (-1,0), (0,-1)]
    m_graph = {}
    m_left = set(m_entrances)
    while m_left:
        next_node = m_left.pop()
        parse_maze(next_node, m_map, m_dirs, m_graph)
        [m_left.add(n) for n in m_graph[next_node] if not n in m_graph]
    return m_graph

def prune_graph(m_graph, m_map):
    while True:
        dead_ends = [c for c in m_graph if len(m_graph[c]) == 1 and m_map[c] == '.']
        if not dead_ends:
            break
        for dead_end in dead_ends:
            for neigbour in m_graph[dead_end]:
                del m_graph[neigbour][dead_end]
            del m_graph[dead_end]

    to_remove = []
    for (k, v) in m_graph.items():
        if len(v) == 2 and m_map[k] == '.':
            items = [x for x in v.items()]
            p1 = items[0][0]
            p2 = items[1][0]
            l = items[0][1] + items[1][1]
            del m_graph[p1][k]
            m_graph[p1][p2] = l
            del m_graph[p2][k]
            m_graph[p2][p1] = l
            to_remove.append(k)

    for p in to_remove:
        del m_graph[p]

def get_shortest_paths_rec(m_pos, m_walked, m_graph, m_map, m_keys, m_doors, m_visited):
    if m_pos in m_visited and m_visited[m_pos] < m_walked:
        return
    m_visited[m_pos] = m_walked
    c = m_map[m_pos]
    if c.islower():
        m_keys[c] = (m_walked, m_doors)
    if c.isupper():
        m_doors += c.lower() # to lower to be able to match easier
    for m_next in m_graph[m_pos].items():
        get_shortest_paths_rec(m_next[0], m_walked + m_next[1], m_graph, m_map, m_keys, m_doors, m_visited)

def get_shortest_paths(m_start, m_graph, m_map):
    m_keys = {}
    get_shortest_paths_rec(m_start, 0, m_graph, m_map, m_keys, '', {})
    return m_keys

def transform_graph(m_graph, m_map, m_keys, m_entrances):
    m_new_graph = {}
    for (k, v) in m_keys.items():
        m_new_graph[k] = get_shortest_paths(v, m_graph, m_map)
        del m_new_graph[k][k]
    for m_pos in m_entrances:
        m_new_graph[m_pos] = get_shortest_paths(m_pos, m_graph, m_map)
    return m_new_graph

def is_locked(m_keys, m_doors):
    for d in m_doors:
        if d not in m_keys:
            return True
    return False

def get_shortest_key_path(m_pos_list, m_pos_index, m_graph, m_walked, m_keys, m_visited, all_keys):
    if m_keys == all_keys:
        if all_keys in m_visited and m_visited[all_keys] <= m_walked:
            return
        print('Found shortest: %i' % m_walked)
        m_visited[all_keys] = m_walked
        return
    current_status = (tuple(m_pos_list), m_keys)
    if current_status in m_visited and m_visited[current_status] <= m_walked:
        return
    m_visited[current_status] = m_walked
    for m_pos_index in range(len(m_pos_list)):
        m_pos = m_pos_list[m_pos_index]
        for (m_key, (m_dist, m_doors)) in m_graph[m_pos].items():
            if m_key in m_keys or is_locked(m_keys, m_doors):
                continue
            old_pos = m_pos_list[m_pos_index]
            m_pos_list[m_pos_index] = m_key
            get_shortest_key_path(m_pos_list, m_pos_index, m_graph, m_walked + m_dist, ''.join(sorted(m_keys + m_key)), m_visited, all_keys)
            m_pos_list[m_pos_index] = old_pos

def solve_maze(m_map, m_keys, m_entrances):
    m_graph = get_graph(m_map, m_entrances)

    print('Nodes before prune: %i' % len(m_graph))
    prune_graph(m_graph, m_map)

    print('Nodes after prune: %i' % len(m_graph))

    m_graph = transform_graph(m_graph, m_map, m_keys, m_entrances)

    m_visited = {}
    all_keys = ''.join(sorted(m_keys.keys()))
    get_shortest_key_path(m_entrances, 0, m_graph, 0, '', m_visited, all_keys)
    print(m_visited[all_keys])

def mod_map(m_map, m_entrance):
    (x, y) = m_entrance
    m_entrances = [(x + 1, y + 1), (x + 1, y - 1), (x - 1, y - 1), (x - 1, y + 1)]
    m_map[(x + 1, y)] = '#'
    m_map[(x, y + 1)] = '#'
    m_map[(x - 1, y)] = '#'
    m_map[(x, y - 1)] = '#'
    m_map[(x, y)] = '#'
    for p in m_entrances:
        m_map[p] = '@'
    return m_entrances

def main():
    m_filename = 'day18_input.txt'
    with open(m_filename, 'r') as f:
        m_text = f.read()

    (m_map, m_keys, m_entrance) = get_map_and_nodes(m_text)

    print('Day 18 part 1')
    solve_maze(m_map, m_keys, [m_entrance])

    print('Day 18 part 2')
    m_entrances = mod_map(m_map, m_entrance)
    solve_maze(m_map, m_keys, m_entrances)

if __name__ == "__main__":
    main()
