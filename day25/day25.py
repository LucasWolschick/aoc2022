import sys
import math

numbers = []
for l in sys.stdin.readlines():
    l = l.strip()
    if not l.isspace():
        numbers.append(l)

def snafu_to_dec(snafu):
    accum = 0
    i = 0
    while i < len(snafu):
        c = snafu[-i-1] 
        p = 5**i
        if c == "2":
            accum += 2*p
        elif c == "1":
            accum += 1*p
        elif c == "0":
            pass
        elif c == "-":
            accum += -1*p
        elif c == "=":
            accum += -2*p
        i += 1
    return accum

def dec_to_base5(dec):
    if dec < 0:
        return "-" + dec_to_base5(-dec)
    if dec == 0:
        return "0"

    digits = []
    accum = dec
    dits = math.floor(math.log(dec, 5))
    for i in reversed(range(dits + 1)):
        amt = accum // (5**i)
        accum -= amt*5**i
        digits.append(str(amt))
    return "".join(digits)

def base5_to_snafu(b5):
    digits = [int(c) for c in b5]

    carry = 0
    i = len(digits)-1

    while i >= 0:
        if carry > 0:
            digits[i] += carry
            carry = 0
            if digits[i] >= 5:
                carry = digits[i]//5
                digits[i] = digits[i] % 5
        if digits[i] == 3:
            digits[i] = "="
            carry = 1
        elif digits[i] == 4:
            digits[i] = "-"
            carry = 1
        else:
            digits[i] = str(digits[i])
        i -= 1

    return "".join(digits)

def dec_to_snafu(dec):
    return base5_to_snafu(dec_to_base5(dec))

# part 1
s = sum(snafu_to_dec(d) for d in numbers)
print(dec_to_snafu(s))
