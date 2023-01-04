import math
import sys
import re

lines = []
for data in sys.stdin.readlines():
    if data.strip() != "":
        grep = re.search(r"Sensor at x=([^,]+), y=([^,]+): closest beacon is at x=([^,]+), y=([^,]+)", data)
        sensor = (int(grep.group(1)), int(grep.group(2)))
        beacon = (int(grep.group(3)), int(grep.group(4)))
        lines.append((sensor, beacon))

def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# part 1
def coverage(y):
    beacons_in_y = set() 
    intervals = []
    
    for sensor, beacon in lines:
        if beacon[1] == y:
            beacons_in_y.add(beacon[0])

        dist = distance(sensor, beacon)
        dy = abs(y - sensor[1])
        dx = dist - dy
        if dx >= 0:
            intervals.append(((sensor[0] - dx), (sensor[0] + dx)))

    # collapse overlapping intervals
    intervals = collapse_ranges(intervals)
    cov = sum(map(lambda x: x[1] - x[0] + 1, intervals)) - len(beacons_in_y)

    return max(cov, 0)

def collapse_ranges(intervals):
    intervals = sorted(intervals)
    i = 0
    while i < len(intervals) - 1:
        j = i + 1 
        while j < len(intervals):
            if intervals[i][0] <= intervals[j][0] <= intervals[i][1]:
                # extend to cover overlapping interval
                intervals[i] = (intervals[i][0], max(intervals[i][1], intervals[j][1]))
                intervals.pop(j)
            else:
                break
        i += 1
    return intervals


print(coverage(10))
print(coverage(2000000))

MAX_RANGE = 4000000

# part 2
def solve():
    # the solution is on the perimeter of a sensor
    candidates = set() 
    j = 0
    for sensor, beacon in lines:
        radius = distance(sensor, beacon)
        j += 1
        print('scanning', j, 'radius', radius)
        for i in range(radius+1):
            points = [
                (sensor[0] + radius + 1 - i, sensor[1] + i),
                (sensor[0] - i, sensor[1] + radius + 1 - i),
                (sensor[0] - radius - 1 + i, sensor[1] - i),
                (sensor[0] + i, sensor[1] - radius - 1 + i),
            ]
            for point in points:
                if 0 <= point[0] <= MAX_RANGE and 0 <= point[1] <= MAX_RANGE:
                    away = True
                    for s, b in lines:
                        if distance(s, point) <= distance(s, b):
                            away = False
                            break
                    if away:
                        return point

s = solve()
print(s[0] * MAX_RANGE + s[1])
