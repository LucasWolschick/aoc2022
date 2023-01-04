import sys
import math

class Directory:
    name: str
    files: list["File"]
    dirs: list["Directory"]
    parent: "Directory"

    def __init__(self, name, parent=None):
        self.files = []
        self.dirs = []
        self.parent = parent
        self.name = name
    
    def __repr__(self):
        return self.name + "(dir) (%d)" % (self.size(), )

    def size(self):
        s = sum(map(lambda x: x.size, self.files))
        for d in self.dirs:
            s += d.size()
        return s

    def add_dir(self, directory):
        self.dirs.append(directory)
        directory.parent = self

    def add_file(self, file):
        self.files.append(file)

    def print_tree(self, level=0):
        print("  " * level + self.name + " (dir) (%d)" % self.size())
        for f in self.files:
            print("  " * (level + 1) + f.name + " (file) (%d)" % f.size)
        for d in self.dirs:
            d.print_tree(level+1)
        

class File:
    size: int
    name: str

    def __init__(self, name, sz):
        self.name = name
        self.size = sz

# parse commands
inputs = []
CD, LS, DIR, FILE = ["CD", "LS", "DIR", "FILE"]
s = sys.stdin.read()
for line in s.splitlines():
    line = line.strip()
    if line.startswith("$ cd"):
        inputs.append((CD, line[5:]))
    elif line.startswith("$ ls"):
        inputs.append((LS,))
    elif line.startswith("dir"):
        inputs.append((DIR, line[4:]))
    elif line != "":
        sz, name = line.split(" ")
        sz = int(sz)
        inputs.append((FILE, sz, name))

# build tree
root = Directory("/")
wd = None
for command in inputs:
    match command:
        case ("CD", path):
            # change our path
            if path == "/":
                wd = root
            elif path == "..":
                if not wd.parent:
                    wd = root
                else:
                    wd = wd.parent
            else:
                for d in wd.dirs:
                    if d.name == path:
                        wd = d
                        break
        case ("LS",):
            # ignore, really
            pass
        case ("DIR", name):
            # create a new directory and append it to our wd
            d = Directory(name)
            wd.add_dir(d)
        case ("FILE", sz, name):
            # create a new file and append it to our wd
            f = File(name, sz)
            wd.add_file(f)


# part 1
def count(d, s, sz=100000):
    if d.size() < sz:
        s.add(d)
    for dc in d.dirs:
        count(dc, s, sz)
lesser = set()
count(root, lesser)
print(sum(map(lambda x: x.size(), iter(lesser))))

# part 2
total_size = root.size()
remaining = 70000000 - total_size
needed = 30000000
diff = needed - remaining
alles = set()
count(root, alles, math.inf)
dirs = list(iter(alles))
dirs.sort(key=lambda x: x.size())
for d in dirs:
    if d.size() > diff:
        print(d.size())
        break
