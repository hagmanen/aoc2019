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

def find_keys(m_graph, m_map, m_pos, visited, keys_found, steps, max_steps): # => key : (pos, dist)
    found_keys = {}
    if steps > max_steps:
        return found_keys
    for neighbour in m_graph[m_pos]:
        if neighbour in visited:
            continue
        if m_map[neighbour].isupper() and not m_map[neighbour].lower() in keys_found:
            continue
        if m_map[neighbour].islower() and not m_map[neighbour].lower() in keys_found:
            found_keys[m_map[neighbour]] = (neighbour,  steps + m_graph[m_pos][neighbour])
            continue
        for (found_key, where) in find_keys(m_graph, m_map, neighbour, visited.union({m_pos}), keys_found, steps + m_graph[m_pos][neighbour], max_steps).items():
            if found_key in found_keys and where[1] > found_keys[found_key][1]:
                continue
            found_keys[found_key] = where
    return found_keys


def find_shorted_path(m_graph, m_map, m_poses, keys_left, keys_found, travelled, shortest_found):
    if not keys_left:
        print('%s after %i steps' % (keys_found, travelled), flush = True)
        return travelled
    new_keys = {}
    
    for m_pos in m_poses:
        new_keys[m_pos] = {}
        for neighbour in m_graph[m_pos]:
            if m_graph[m_pos][neighbour] + travelled > shortest_found:
                #print('Gaveup %s' % keys_found)
                continue
            if m_map[neighbour].isupper() and not m_map[neighbour].lower() in keys_found:
                continue
            if m_map[neighbour].islower() and not m_map[neighbour].lower() in keys_found:
                new_keys[m_pos][m_map[neighbour]] = (neighbour, m_graph[m_pos][neighbour])
                continue
            for (found_key, where) in find_keys(m_graph, m_map, neighbour, {m_pos}, keys_found, m_graph[m_pos][neighbour], shortest_found - travelled).items():
                if found_key in new_keys[m_pos] and where[1] > new_keys[m_pos][found_key][1]:
                    continue
                new_keys[m_pos][found_key] = where
    result = []
    for m_pos in m_poses:
        new_poses = copy.copy(m_poses)
        new_poses.remove(m_pos)
        for (new_key, where) in new_keys[m_pos].items():
            #print('From %s got to %s, %i steps travelled' % (keys_found, where, travelled))
            new_poses.add(where[0])
            result.append(find_shorted_path(m_graph, m_map, new_poses, keys_left - 1, keys_found + new_key, where[1] + travelled, shortest_found))
            new_poses.remove(where[0])
            shortest_found = min(shortest_found, result[-1])
    return shortest_found

def find_all_keys_from(m_graph, m_map, m_pos, passed_doors, visited, m_already_walked):
    m_keys = {}
    for (neighbour, distance) in m_graph[m_pos].items():
        if neighbour in visited:
            continue
        if m_map[neighbour].islower():
            m_keys[m_map[neighbour]] = (m_already_walked + distance, passed_doors)
        for (m_key, m_value) in find_all_keys_from(m_graph,
                                        m_map,
                                        neighbour,
                                        passed_doors + (m_map[neighbour].lower() if m_map[neighbour].isupper() else ''),
                                        visited.union({neighbour}),
                                        m_already_walked + distance).items():
            if m_key in m_keys and m_keys[m_key][0] < m_value[0]:
                continue
            if m_key in m_keys and m_keys[m_key][0] >= m_value[0]:
                print('Overwrite %s with %s for %s' % (str(m_keys[m_key]), str(m_value), m_key))
            m_keys[m_key] = m_value
    return m_keys

def have_keys(m_doors, m_keys):
    for m_door in m_doors:
        if not m_door in m_keys:
            return False
    return True

def find_shortest(m_stuff, m_pos, found_keys, shortest_found, walked, m_cache):
    if walked > shortest_found:
        return (shortest_found + 1)
    #cache_key = m_pos + ''.join(sorted(found_keys))
    #if cache_key in m_cache:
    #    return (walked + m_cache[cache_key])
    nothing_left = True
    for (m_key, m_value) in m_stuff[m_pos].items():
        if not m_key in found_keys and have_keys(m_value[1], found_keys):
            nothing_left = False
            shortest_found = min(shortest_found,find_shortest(m_stuff, m_key, found_keys + m_key, shortest_found, walked + m_value[0], m_cache))
    if nothing_left:
        print('shortest %s in %i' % (found_keys, walked))
        #m_cache[cache_key] = 0
        return walked
    #m_cache[cache_key] = (shortest_found - walked)
    return shortest_found

def main():
    m_filename = 'day18_input.txt'
    with open(m_filename, 'r') as f:
        m_text = f.read()

    m_dirs = [(1,0), (0,1), (-1,0), (0,-1)]
    m_map = {}
    m_entrance = None
    m_keys = {}
    y = 0
    for line in m_text.splitlines():
        x = 0
        for c in line:
            if c == '#':
                pass
            elif c == '@':
                m_entrance = (x, y)
                m_map[(x, y)] = c
            else:
                if c.islower():
                    m_keys[c] = (x, y)
                m_map[(x, y)] = c
            x += 1
        y += 1

    m_graph = {}
    m_left = {m_entrance}
    while m_left:
        next_node = m_left.pop()
        parse_maze(next_node, m_map, m_dirs, m_graph)
        [m_left.add(n) for n in m_graph[next_node] if not n in m_graph]

    print('Nodes before prune: %i' % len(m_graph))
    while True:
        dead_ends = [c for c in m_graph if len(m_graph[c]) == 1 and m_map[c] == '.']
        if not dead_ends:
            break
        for dead_end in dead_ends:
            for neigbour in m_graph[dead_end]:
                del m_graph[neigbour][dead_end]
            del m_graph[dead_end]

    print('Nodes after prune: %i' % len(m_graph))

    m_stuff = {}
    m_stuff['@'] = find_all_keys_from(m_graph, m_map, m_entrance, '', {m_entrance}, 0)
    for (m_key, m_pos) in m_keys.items():
        m_stuff[m_key] = find_all_keys_from(m_graph, m_map, m_pos, '', {m_pos}, 0)

    m_cache = {}
    print(find_shortest(m_stuff, '@', '@', 100000, 0, m_cache))
    #print(m_cache)
    '''
    m_map[m_entrance] = '#'
    m_map[(m_entrance[0] + 1, m_entrance[1] + 1)] = '@'
    m_map[(m_entrance[0] + 1, m_entrance[1] - 1)] = '@'
    m_map[(m_entrance[0] - 1, m_entrance[1] + 1)] = '@' 
    m_map[(m_entrance[0] - 1, m_entrance[1] - 1)] = '@'
    m_map[(m_entrance[0] + 1, m_entrance[1])] = '#'
    m_map[(m_entrance[0] - 1, m_entrance[1])] = '#'
    m_map[(m_entrance[0], m_entrance[1] + 1)] = '#'
    m_map[(m_entrance[0], m_entrance[1] - 1)] = '#'
    m_graph = {}
    m_entrances = {(m_entrance[0] + 1, m_entrance[1] + 1),
                   (m_entrance[0] + 1, m_entrance[1] - 1),
                   (m_entrance[0] - 1, m_entrance[1] + 1),
                   (m_entrance[0] - 1, m_entrance[1] - 1)}
    m_left = copy.copy(m_entrances)
    while m_left:
        next_node = m_left.pop()
        parse_maze(next_node, m_map, m_dirs, m_graph)
        [m_left.add(n) for n in m_graph[next_node] if not n in m_graph]


    print(find_shorted_path(m_graph, m_map, m_entrances, nr_of_keys, '', 0, 10000000))
    #print(m_graph)
    '''
if __name__ == "__main__":
    main()
