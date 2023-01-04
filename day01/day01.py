data = []
v = []
try:
    while True:
        s = input()
        if s.strip() == "":
            data.append(v)
            v = []
        else:
            v.append(int(s))
except EOFError:
    pass
if len(v) > 0:
    data.append(v)

# part 1
data2 = [sum(s) for s in data]
print("day1 1/2: ", max(data2))

# part 2
data2.sort(reverse=True) 
print("day1 2/2: ", sum(data2[0:3]))
