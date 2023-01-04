data = input().strip()

# part 01
for i in range(len(data)-4):
    c = set(data[i:i+4])
    if len(c) == 4:
        print("start at: ", i + 4)
        break

# part 02
for i in range(len(data)-14):
    c = set(data[i:i+14])
    if len(c) == 14:
        print("start at: ", i + 14)
        break

