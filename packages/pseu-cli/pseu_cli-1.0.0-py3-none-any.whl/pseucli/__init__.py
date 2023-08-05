#!/usr/bin/env python3

import argparse
import re
import random
import sys

BASE64_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/"

ROLL_REG = re.compile("^([1-9][0-9]*)d([1-9][0-9]*)$")

JUST_NUM_RAND_REG = re.compile("^[1-9][0-9]*$")
DASH_RAND_REG = re.compile("^([0-9]+)-([0-9]+)(x([1-9][0-9]*))?$")

class CliError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

def out(msg, *fmt_args):
    print(msg.format(*fmt_args))

def out_error(msg):
    print(
        make_red_if_appropriate("ERROR! ", sys.stderr) + msg,
        file=sys.stderr)

def make_red_if_appropriate(s, stream):
    if stream.isatty():
        return "\033[31m" + s + "\033[0m"
    # Not a terminal, doesn't make sense to use
    # the terminal formatting codes.
    return s

def roll(rnd, raw_dices, stats):
    do_rand(
        rnd,
        [Range(1, 1, 6)]
            if not raw_dices
            else [parse_dice(s) for s in raw_dices],
        stats)

def parse_dice(s):
    match = ROLL_REG.match(s)
    if not match:
        raise CliError("Invalid dice format: " + s)
    return Range(
        int(match.group(1)),
        1,
        int(match.group(2)))

class Range:
    def __init__(self, times, lb, ub):
        self.times = times
        self.lb = lb
        self.ub = ub

    def get_nums(self, rnd):
        return [rnd.randint(self.lb, self.ub) for _ in range(self.times)]

    def __eq__(self, other):
        return (isinstance(other, Range)
                and self.times == other.times
                and self.lb == other.lb
                and self.ub == other.ub)

def parse_range(s):
    m = JUST_NUM_RAND_REG.match(s)
    if m:
        return Range(1, 0, int(s)-1)
    m = DASH_RAND_REG.match(s)
    if m:
        lb = int(m.group(1))
        ub = int(m.group(2))
        if lb > ub:
            raise CliError("Invalid range '{}', lower bound must be greater than or equal to upper bound".format(s))
        return Range(int(m.group(4)) if m.group(4) else 1, lb, ub)
    raise CliError("Invalid range: " + s)

def rand(rnd, raw_ranges, stats):
    do_rand(
        rnd,
        [Range(1, 0, 2**16-1)]
            if not raw_ranges
            else [parse_range(s) for s in raw_ranges],
        stats)

def do_rand(rnd, ranges, stats):
    results = []
    for r in ranges:
        for n in r.get_nums(rnd):
            results.append(n)
    out(" ".join(map(str, results)))
    if stats:
        out("sum: {}", sum(results))
        out("max: {}", max(results))
        out("min: {}", min(results))

def pick(rnd, n, words):
    things = get_things(words)
    sampled = things if n > len(things) else rnd.sample(things, n)
    for s in sampled:
        out(s)

def shuffle(rnd, words):
    things = get_things(words)
    rnd.shuffle(things)
    for s in things:
        out(s)

def get_things(words):
    return words or [line.strip() for line in sys.stdin.readlines()]

class Arg:
    def __init__(self, name, *args, **kwargs):
        self.name = name.lstrip("-")
        self.raw_name = name
        self.args = args
        self.kwargs = kwargs

STATS_ARG = Arg(
    "--stats",
    default=False,
    action="store_true",
    help="whether to print stats (sum, max, min)")

def get_words_arg(infinitive, participle):
    return Arg(
        "words",
        nargs="*",
        help="the words to {}; alternatively, input can be passed through standard input, and lines will be {}".format(infinitive, participle))

SUBCOMMANDS = [
    ("roll",
     "roll dice",
     roll,
     [Arg("dice", nargs="*", help="dice rolls, in the form {n}d{m}; 1d6 by default"),
      STATS_ARG]),
    ("rand",
     "generate random numbers",
     rand,
     [Arg(
        "range",
        nargs="*",
        help="number range; {n}-{m} (for n,n+1,...,m), {n}-{m}x{t} (same, but 't' times), or {n} (for 0,1,...,n-1); 0,1,...,2^16-1 by default"),
      STATS_ARG]),
    ("pick",
     "pick from a selection of words or lines",
     pick,
     [Arg(
        "--n",
        default=1,
        required=False,
        type=int,
        help="number of words/lines to pick"),
      get_words_arg("pick from", "picked")]),
    ("shuffle",
     "shuffle words or lines",
     shuffle,
     [get_words_arg("shuffle", "shuffled")])
]

def get_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    for name, description, f, args in SUBCOMMANDS:
        add_subparser(subparsers, name, description, f, args)
    return parser

def add_subparser(subparsers, name, description, f, args):
    parser = subparsers.add_parser(name, help=description)
    for arg in args:
        parser.add_argument(arg.raw_name, *arg.args, **arg.kwargs)
    parser.add_argument(
        "--seed",
        required=False,
        help="base-64 seed, digits [0-9A-Za-z+/]")
    def wrapped_func(cli_args):
        try:
            if cli_args.seed:
                r = random.Random(parse_base64_seed(cli_args.seed))
            else:
                r = random.Random()
            f(r, *[getattr(cli_args, arg.name) for arg in args])
        except Exception as e:
            out_error(e.message)
            sys.exit(1)
    parser.set_defaults(func=wrapped_func)

def parse_base64_seed(s):
    result = 0
    for i, c in enumerate(reversed(s)):
        try:
            result += BASE64_CHARS.index(c) * (64**i)
        except ValueError as e:
            raise CliError("Seed must be base64 (characters [0-9A-Ba-b+/])")
    return result

def main():
    parser = get_parser()
    if len(sys.argv) == 1:
        # argparse doesn't handle it well when there
        # are no arguments.
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
