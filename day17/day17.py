import sys
import math

ROCKS = [
    "####",

    """.#.
       ###
       .#.""",

    """..#
       ..#
       ###""",

    """#
       #
       #
       #""",

    """##
       ##"""
]
class Pattern:
    def __init__(self, pat):
        lines = [l.strip() for l in pat.splitlines() if l.strip() != ""]
        lines = [[c == "#" for c in l] for l in lines]
        self.lines = []
        for y in lines:
            for x in y:
                self.lines.append(x)
        self.width = len(lines[0])
        self.height = len(lines)

    def get(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.lines[y*self.width + x]

ROCKS = [Pattern(pat) for pat in ROCKS]

class Rock:
    def __init__(self, pat, x=2, y=0):
        self.pat = pat
        self.x = x 
        self.y = y
        self.height = pat.height
        self.width = pat.width

    def test(self, x, y):
        nx = x - self.x
        ny = self.y - y 
        return self.pat.get(nx, ny)
    
    def move(self, dx, dy):
        return Rock(self.pat, self.x + dx, self.y + dy)

    def height(self):
        return self.height

    def width(self):
        return self.width

class Board:
    def __init__(self, width, height):
        self.mat = [False]*width*height
        self.width = width
        self.height = height
        self.tallest = -1 

    def get(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return self.mat[y*self.width+x]

    def set(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.mat[y*self.width+x] = True
            if y > self.tallest:
                self.tallest = y
        else:
            print('set out of bounds')

    def string(self, rock=None):
        lines = []
        
        upper = self.tallest+1
        if rock and rock.y+1 > upper and rock.y+1 <= self.height:
            upper = rock.y+1

        for y in reversed(range(0, upper)):
            s = "|"
            for i in self.width:
                x = self.mat[y*self.width + i]
                symbol = "#" if x else "."
                if rock and rock.test(i, y):
                    symbol = "@"
                s += symbol
            s += "|"
            lines.append(s)

        lines.append("+" + "-" * self.width + "+")

        return "\n".join(lines)
    
    def __repr__(self):
        return self.string()

moves = sys.stdin.read().strip()

def board_rock_intersect(board, rock):
    if 0 <= rock.x < rock.x + rock.width <= board.width and rock.y - rock.height > board.tallest:
        return False
    for y in range(rock.y - rock.height+1, rock.y+1):
        for x in range(rock.x, rock.x + rock.width):
            if rock.test(x, y) and board.get(x, y):
                return True
    return False

def fill_board(board, rock):
    for y in range(rock.y - rock.height+1, rock.y+1):
        for x in range(rock.x, rock.x + rock.width):
            if rock.test(x, y):
                board.set(x, y)

# part 1
#   |      |
#   |      |
#   |y     |
#   |^     |
#   |+> x  |
#   +------+
#    
#
def calc_height(n, max_h=None):
    max_h = max_h or n*7
    board = Board(7, max_h) 
    rock_i = 0
    jet_i = 0

    for i in range(n):
        rock = Rock(ROCKS[rock_i], 2, board.tallest + 3 + ROCKS[rock_i].height)
        rock_i = (rock_i + 1) % len(ROCKS) 
        while True:
            # push
            gas = 1 if moves[jet_i] == ">" else -1
            jet_i = (jet_i + 1) % len(moves)
            rockd = rock.move(gas, 0)
            if not board_rock_intersect(board, rockd):
                rock = rockd

            # fall
            rockd = rock.move(0, -1)
            if not board_rock_intersect(board, rockd):
                rock = rockd
            else:
                break
        # freeze
        fill_board(board, rock)

    return board.tallest + 1

def get_surface(board):
    out = [0]*board.width
    for x in range(board.width):
        for y in reversed(range(0, board.tallest)):
            if board.get(x, y):
                out[x] = y+1
                break
    return tuple(board.tallest - h for h in out) 

def gcd(a,b):
    while b != 0:
        t = b
        b = a % b
        a = t
    return a

def lcm(a,b):
    return abs(a*b)//gcd(a,b)

# part 1
print('part 1:', calc_height(2022))

# part 2
LARGE_NUMBER = 1_000_000_000_000

def find_loop(max_h=100000):
    board = Board(7, max_h) 
    rock_i = 0
    jet_i = 0
    states = {}

    i = 0

    while True:
        i += 1

        state = (rock_i-1, jet_i-1, get_surface(board))
        if state in states:
            return states[state], i
        states[state] = i

        rock = Rock(ROCKS[rock_i], 2, board.tallest + 3 + ROCKS[rock_i].height)
        rock_i = (rock_i + 1) % len(ROCKS) 
        while True:
            # push
            gas = 1 if moves[jet_i] == ">" else -1
            jet_i = (jet_i + 1) % len(moves)
            rockd = rock.move(gas, 0)
            if not board_rock_intersect(board, rockd):
                rock = rockd

            # fall
            rockd = rock.move(0, -1)
            if not board_rock_intersect(board, rockd):
                rock = rockd
            else:
                break
        # freeze
        fill_board(board, rock)
        

first, second = find_loop(10000000)
period = second - first
diff = calc_height(first + period) - calc_height(first)

wholes = (LARGE_NUMBER - first) // period
remainder = (LARGE_NUMBER - first) % period

base_i = first 
base = calc_height(base_i)
extra = calc_height(base_i + remainder) - calc_height(base_i) 

total = wholes*diff + extra + base 

print(total)
