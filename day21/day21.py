import sys
import math
import string
import re
import copy

# RULE ::= NAME: (NAME (+|-|*|/) NAME) | NUMBER
# NAME ::= [a-z]+
# NUMBER ::= [0-9]+

class Node:
    name: str

    def __repr__(self):
        return "Node " + self.name

class LiteralNode(Node):
    value: int
    
    def __init__(self):
        Node.__init__(self)

    def __repr__(self):
        return str(self.value) 

class BinaryNode(Node):
    lhs: Node
    op: str
    rhs: Node

    def __init__(self):
        Node.__init__(self)

    def __repr__(self):
        return f"({self.op} {self.lhs} {self.rhs})"

# build nodes
nodes = {}
for rule in sys.stdin.readlines():
    rule = rule.strip()

    if rule.strip() == "":
        continue

    name, tail = rule.split(": ")
    if tail[0] in string.digits:
        # parse literal node 
        l = LiteralNode()
        l.value = int(tail)
        l.name = name

        nodes[name] = l
    else:
        # parse binary rule
        m = re.match(r"(\w+) ([\+\-\*\/]) (\w+)", tail.strip())
        l, op, r = m.group(1), m.group(2), m.group(3)
        
        b = BinaryNode()
        b.name = name
        b.lhs = Node()
        b.lhs.name = l
        b.rhs = Node()
        b.rhs.name = r
        b.op = op

        nodes[name] = b

# part 1
nodes1 = copy.deepcopy(nodes)
# replace node references by real nodes
for k in nodes1.keys():
    if isinstance(nodes1[k], BinaryNode):
        nodes1[k].lhs = nodes1[nodes1[k].lhs.name]
        nodes1[k].rhs = nodes1[nodes1[k].rhs.name]

# evaluate tree (part 1)
def evaluate(node):
    if isinstance(node, LiteralNode):
        return node.value
    elif isinstance(node, BinaryNode):
        lhs = evaluate(node.lhs)
        rhs = evaluate(node.rhs)
        match node.op:
            case "+":
                return lhs + rhs
            case "-":
                return lhs - rhs
            case "*":
                return lhs * rhs
            case "/":
                return lhs / rhs
            case _:
                raise Exception("Invalid operation")

print(evaluate(nodes1["root"]))

# part 2
# replace humn node by a HumanNode
class HumanNode(Node):
    def __init__(self):
        Node.__init__(self)

    def __repr__(self):
        return "x"

nodes["humn"] = HumanNode()
nodes["humn"].name = "humn"

# replace node references by real nodes
for k in nodes.keys():
    if isinstance(nodes[k], BinaryNode):
        nodes[k].lhs = nodes[nodes[k].lhs.name]
        nodes[k].rhs = nodes[nodes[k].rhs.name]


def find_variable(node):
    if isinstance(node, HumanNode):
        return True
    elif isinstance(node, BinaryNode):
        return find_variable(node.lhs) or find_variable(node.rhs)
    else:
        return False

# preprocess
root = nodes["root"]
if not find_variable(root.lhs):
    root.lhs, root.rhs = root.rhs, root.lhs

# the variable is on the left
while not isinstance(root.lhs, HumanNode):
    b = root.lhs
    on_left = find_variable(b.lhs)
    nb = BinaryNode()
    nb.name = b.name
    match b.op:
        case "+":
            if on_left:
                # throw rhs to right side of eq as a -
                nb.lhs = root.rhs
                nb.op = "-"
                nb.rhs = b.rhs

                root.rhs = nb
                root.lhs = b.lhs
            else:
                # throw lhs to right side of eq as a -
                nb.lhs = root.rhs
                nb.op = "-"
                nb.rhs = b.lhs

                root.rhs = nb
                root.lhs = b.rhs
        case "-":
            if on_left:
                # throw rhs to right side of eq as a +
                nb.lhs = root.rhs
                nb.op = "+"
                nb.rhs = b.rhs

                root.rhs = nb
                root.lhs = b.lhs
            else:
                # convert (- a b) to (+ a (* b -1)) then proceed as usual
                b.op = "+"
                
                nb.name += "INV"
                nb.lhs = b.rhs
                nb.op = "*"
                nb.rhs = LiteralNode()
                nb.rhs.name = nb.name + "NEG"
                nb.rhs.value = -1

                b.rhs = nb

        case "*":
            if on_left:
                # throw rhs to right side of eq as a /
                nb.lhs = root.rhs
                nb.op = "/"
                nb.rhs = b.rhs

                root.rhs = nb
                root.lhs = b.lhs
            else:
                # throw lhs to right side of eq as a /
                nb.lhs = root.rhs
                nb.op = "/"
                nb.rhs = b.lhs

                root.rhs = nb
                root.lhs = b.rhs
            
        case "/":
            if on_left:
                # throw rhs to right side of eq as a *
                nb.lhs = root.rhs
                nb.op = "*"
                nb.rhs = b.rhs

                root.rhs = nb
                root.lhs = b.lhs
            else:
                # throw rhs to right side of eq as a *
                nb.lhs = root.rhs
                nb.op = "*"
                nb.rhs = b.rhs
                root.rhs = nb
                root.lhs = b.lhs
                # then flip around
                root.rhs, root.lhs = root.lhs, root.rhs

print(nodes["root"])
print(evaluate(root.rhs))
