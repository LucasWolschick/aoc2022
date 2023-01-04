import string
import sys
from functools import cmp_to_key

# input = list '\n' list '\n'+
# list = '[' (list | number)* ']'

def tokenize(data):
    current = 0
    tokens = []
    while current < len(data):
        word = data[current]
        if word == "[":
            tokens.append("[") 
        elif word == "]":
            tokens.append("]")
        elif word == "\n":
            tokens.append("l")
        elif word in string.digits:
            begin = current
            while current < len(data) and data[current] in string.digits:
                current += 1
            tokens.append(int(data[begin:current]))
            current -= 1
        else:
            pass
        current += 1

    return tokens

def parse(tokens):
    current = 0
    lists = []
    stack = []

    def previous():
        if current > 0:
            return tokens[current - 1]

    def advance():
        nonlocal current
        if current < len(tokens):
            current += 1
        return previous()

    def check(tok):
        if current < len(tokens):
            if tok == "Number":
                return type(tokens[current]) == int
            else:
                return tokens[current] == tok
        return False

    def match(tok):
        if check(tok):
            advance()
            return True
        return False

    def consume(tok, err):
        if check(tok):
            return advance()
        raise err

    def data():
        nonlocal lists
        a = lisp()
        consume('l', "Expected line separator")
        b = lisp()
        consume('l', "Expected line separator")
        while (match('l')):
            pass
        lists.append((a, b))
    
    def lisp():
        consume('[', "Expected [ in input")
        return lispBody()

    def lispBody():
        l = []
        while (match("Number") or match("[")):
            if previous() == "[":
                l.append(lispBody())
            else:
                l.append(previous())
        consume("]", "Expected closing ]")
        return l
    
    while current < len(tokens):
        data()

    return lists

# overengineered parser!!!!
data = sys.stdin.read()
tokens = tokenize(data)
lists = parse(tokens)

# part 1
OK, IDK, NG = [-1, 0, 1]

def decideNumbers(l, r):
    if l < r:
        return OK
    elif l > r:
        return NG
    else:
        return IDK

def decideLists(l, r):
    i = 0
    while i < len(l) and i < len(r):
        a, b = l[i], r[i]
        resp = decide(a, b)
        if resp != IDK:
            return resp
        i += 1
    if len(l) < len(r):
        return OK
    elif len(l) > len(r):
        return NG
    else:
        return IDK

def decide(l, r):
    if type(l) == type(r) == int:
        return decideNumbers(l, r)
    elif type(l) == type(r) == list:
        return decideLists(l, r)
    else:
        if type(l) == list:
            return decide(l, [r])
        elif type(r) == list:
            return decide([l], r)

def validate(entry):
    return decide(entry[0], entry[1]) == OK

s = 0
for i, entry in enumerate(lists):
    if validate(entry):
        s += i+1

print(s)

# part 2
divider_a, divider_b = [[2]], [[6]]
allpackets = [divider_a, divider_b]
for a, b in lists:
    allpackets.append(a)
    allpackets.append(b)

allpackets.sort(key=cmp_to_key(decide))
print((allpackets.index(divider_a) + 1)*(allpackets.index(divider_b) + 1))
