## Description
pseu is a CLI tool that provides the following pseudorandom utilities: picking, shuffling, dice-rolling and number generation. It's useful for people who frequently call on machines to make their life choices.

```
$ pseu pick "good life choice" "bad life choice"
bad life choice
$ pseu pick --n 2 </tmp/movies.txt
Boogie Nights
The Hunt for the Wilderpeople
$ pseu roll 1d6
3
$ pseu rand 100
42
$ pseu shuffle alice sue bob
bob
sue
alice
```

## Setup
Requires Python 3. Install from [PyPI](https://pypi.org/project/pseu-cli/) using pip:

```
pip3 install pseu-cli
```

## More examples
`roll` and `rand` can print stats.

```
$ pseu roll 3d6 --stats
4 5 4
sum: 13
max: 5
min: 4
```

Multiple types of dice, multiple random numbers.

```
$ pseu roll 2d6 6d3
6 6 1 3 3 1 2 1
$ pseu rand 1-3x5 10-20
2 2 1 3 1 16
```

Use a (base64) seed to repeat results.

```
$ pseu 1-1000 --seed abc
903
$ pseu 1-1000 --seed abc
903
```

## Contributing
Feel free to submit tweaks.

To run tests, install tox via `pip3 install tox` and then run the `tox` command from the base directory.
