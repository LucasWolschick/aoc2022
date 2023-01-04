import sys
import math
import re

blueprints = []
for l in sys.stdin.readlines():
    pat = r"Blueprint \d+:\s*Each ore robot costs (\d+) ore.\s*Each clay robot costs (\d+) ore.\s*Each obsidian robot costs (\d+) ore and (\d+) clay.\s*Each geode robot costs (\d+) ore and (\d+) obsidian."
    matches = re.search(pat, l.strip())
    if matches:
        ore_bot = (int(matches.group(1)), 0, 0, 0)
        clay_bot = (int(matches.group(2)), 0, 0, 0)
        obsidian_bot = (int(matches.group(3)), int(matches.group(4)), 0, 0)
        geode_bot = (int(matches.group(5)), 0, int(matches.group(6)), 0)
        blueprints.append((
            ore_bot,
            clay_bot,
            obsidian_bot,
            geode_bot
        ))

stdmax = max
def max(a, b):
    return a if a > b else b

def simulate(bp, minutes):
    # https://www.reddit.com/r/adventofcode/comments/zpy5rm/2022_day_19_what_are_your_insights_and/
    #
    # our search space is based on the "which bot am i going to build next?" decision
    # pruning done:
    # - we do not build more X bots than the largest X cost, as we can only build one robot per round (except if X = ore)
    # - we keep track of our largest geode count seen yet. If the branch cannot generate that many ores even if it
    #   created a new bot every round, then we stop early.
    maximums = [stdmax(proj[i] for proj in bp) for i in range(4)]
    
    best = 0

    # INVARIANT:
    # this function is called at start of minute minutes-t+1.
    # no bots have been built this minute. resources have not been generated yet.
    # in one cycle:
    #   - bots generate resources (1 resource per bot)
    #   - a bot is built (or not)
    def recurse(t, bank, bots):
        nonlocal best
        
        if t <= 0:
            if bank[3] > best:
                best = bank[3]
            return bank[3]

        opt = 0

        # heuristic: see if in the best (unrealistic) case scenario we can exceed the best sofar
        # assume we build a geode bot every round
        # if we have 0 bots, its 0 + 1 + 2 + ... + t geodes until we're done
        upper_bound = bank[3] + bots[3]*t + t*(t-1)/2
        if upper_bound < best:
            return bank[3]
        
        # option 1: build a bot
        for boti, costs in enumerate(bp):
            # if we're already at our max bot count don't bother
            if boti != 3 and maximums[boti] <= bots[boti]:
                continue

            # calculate when this bot would be able to be built
            be_ready_in = -math.inf
            for i in range(4):
                remaining = costs[i] - bank[i]
                rate = bots[i]
                if remaining > 0 and rate == 0:
                    # we can't possibly build this bot
                    be_ready_in = math.inf
                elif rate == 0:
                    # we already have enough of the resource
                    be_ready_in = max(be_ready_in, -math.inf)
                else:
                    # how many minutes until we have enough of the resource?
                    be_ready_in = max(be_ready_in, remaining/rate)

            if be_ready_in == math.inf: 
                continue

            be_ready_in = math.ceil(max(be_ready_in, 0))
            if t-(be_ready_in+1) >= 0:
                nbots = (
                    bots[0] + (boti == 0),
                    bots[1] + (boti == 1),
                    bots[2] + (boti == 2),
                    bots[3] + (boti == 3)
                )
                # skip be_ready_in-1 ticks, build the bot during tick t-be_ready_in, skip that tick.
                nbank = (
                    bank[0] - costs[0] + (be_ready_in+1)*bots[0],
                    bank[1] - costs[1] + (be_ready_in+1)*bots[1],
                    bank[2] - costs[2] + (be_ready_in+1)*bots[2],
                    bank[3] - costs[3] + (be_ready_in+1)*bots[3] 
                )
                opt = max(opt, recurse(t-(be_ready_in+1), nbank, nbots))

        # option 2: wait til time is over with what we've got
        opt = max(opt, recurse(0, (
                bank[0] + t*bots[0],
                bank[1] + t*bots[1],
                bank[2] + t*bots[2],
                bank[3] + t*bots[3]
            ), bots))
       
        return opt
    
    return recurse(minutes, (0, 0, 0, 0), (1, 0, 0, 0))

# part 1
s = 0
for i, bp in enumerate(blueprints):
    v = simulate(bp, 24)
    print('blueprint', i+1, v)
    s += (i+1)*v
print(s)

# part 2
p = 1 
for i, bp in enumerate(blueprints[:3]):
    v = simulate(bp, 32)
    print('blueprint', i+1, v)
    p *= v
print(p)
