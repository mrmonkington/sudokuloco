# Sudokoloco

![Tests](https://github.com/mrmonkington/sudokuloco/workflows/Tests/badge.svg)
[![codecov](https://codecov.io/gh/mrmonkington/sudokuloco/branch/master/graph/badge.svg)](https://codecov.io/gh/mrmonkington/sudokuloco)

A sudoko solver!

Solves 9x9 (n=3, v fast!) and 16x16 (n=4, much less fast) puzzles. 

## Usage

```
git clone https://github.com/mrmonkington/sudokuloco.git
cd sudokuloco
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
python sudokuloco/solver.py < tests/hard_9_1.txt
```

### Input file format

Something like this:

```
4 . . . . . 8 . 5 
. 3 . . . . . . . 
. . . 7 . . . . . 
. 2 . . . . . 6 . 
. . . . 8 . 4 . . 
. . . . 1 . . . . 
. . . 6 . 3 . 7 . 
5 . . 2 . . . . . 
1 . 4 . . . . . .
```

or 

```
8 _ _  _ 9 _  2 5 _
5 _ _  _ 7 _  6 _ 1
_ _ _  8 _ _  _ 9 4

_ 7 5  9 4 _  _ _ _
6 4 _  7 _ 8  _ _ _
_ _ _  _ 2 6  4 7 _

9 2 _  _ _ 4  _ _ _
7 _ 8  _ 1 _  _ _ 2
_ 5 6  _ 8 _  _ _ 9
```

## Development

Run tests:

```
pip install -r dev_requirements.txt
python -m pytest tests/ --cov=sudokuloco
```

Run tests with some diagnostic output
```
python -m pytest tests/ --cov=sudokuloco -vv -s
```

### TODO

 - ~~Speed it up for hard puzzles! The search is extremely naive.~~
 - ~~Not tested (yet!) with 16x16 puzzles (but blindly coded in a size agnostic way)~~ - solved a 16x16 'expert' puzzle in 9m (not great? not sure - don't have a benchmark)
 - Add some launch options and read classic puzzle one-liners from http://magictour.free.fr/top95
 - Tidy up for packaging
