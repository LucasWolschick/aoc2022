sacks = []
separated_sacks = []
try:
    while True:
        data = input().strip()
        if data != "":
            l = data[:len(data)//2]
            r = data[len(data)//2:]
            separated_sacks.append((l, r))
            sacks.append(data)
except EOFError:
    pass

def find_error(pack):
    (l, r) = pack
    l = set(l)
    r = set(r)
    return list(l.intersection(r))[0]

def value(item):
    if 'a' <= item <= 'z':
        return ord(item) - ord('a') + 1
    elif 'A' <= item <= 'Z':
        return ord(item) - ord('A') + 27 
    else:
        return 0

def intersect(trio):
    a, b, c = trio
    a, b, c = set(a), set(b), set(c)
    return list(a.intersection(b).intersection(c))[0]

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

# part 1
print(sum(map(value, map(find_error, separated_sacks))))

# part 2
print(sum(map(value, map(intersect, chunker(sacks, 3))))) 
