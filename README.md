# My Advent of Code 2022 Solutions

This repository contains my solutions to the [Advent of Code 2022](https://adventofcode.com/2022) puzzles.
I managed to finish most of them as they were released, bar a few which were done one or two days later and a couple
which I have only finished weeks after they were out (19 was a particularly egregious one).

The solutions are written in Python 3.11, as I wanted to get some practice with it as it would be required in university work.
Looking back, you can see the coding style evolve as the puzzles were being solved (two things I noticed were moving away from
`input()` to `sys.stdin.read()` and favoring comprehensions over plain function chains).

At the very least I now know a bit more about parsers, search algorithms, pruning and graphs. Oh well.

## Running

The scripts read puzzle data from standard input. Some solutions are actually special-cased to the inputs I've received and may not work on yours or on the example's. These are, as far as I can recall:

 - 19.1, 19.2: The blueprint data must be contained on a single line (the example input is not).
 - 22.2: The second part does not execute on the example input and assumes your map is composed of two stacked Ls. I might revisit this solution in the future.

To run a solution, `cd` into your directory of choice, create a file named `input.txt` with your input data and then execute the following command (or equivalent in your system). (Execute the code at your own risk!)

```bash
$ python3 dayXX.py < input.txt
```

## License

The code in this repository is licensed under the MIT License; the example inputs are copyrighted to Eric Wastl and were fetched from their respective puzzle descriptions. Use this code at your own risk.
