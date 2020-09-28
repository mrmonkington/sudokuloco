"""
    Glossary:
        cell - a space on the puzzle board
        piece - a number (or alphanum or other symbol in 16+ size boards)
        chunksize - the 'fractal' unit of this board, typically 3 (9x9 game) or 4 (16x16)
        row - one chunksize^2 row from left to right, 0 indexed
        col - one chunksize^2 column from top to bottom, 0 indexed
        chunk - the chunksize x chunksize square collection of cells, 0 indexed TL to BR

    algorithm v1:

    each cell is a sequence of possible pieces
    repeat
        iterate through each cell where len(possibilities) > 1
            test each possibilities against row, cell and chunk removing any that fail
            if max(len(possibilities)) == 1
                return solve
            else if no changes this pass
                return unsolvable
"""

import sys
from re import split
import logging
from math import sqrt
import copy

IMPOSSIBLE = -1

BLANKS = ('_', '-', '*', '.')

logging.basicConfig(level=logging.DEBUG)

class FormatException(Exception):
    """Error relating to input file format
    """

class AlgorithmException(Exception):
    """Error relating to algorithm getting into
    unexpected state
    """

def d(str):
    logging.debug(str)

class Puzzle():
    """
        rows -> 0 indexed starting from top
        cols -> 0 indexed starting from left
    """
    def __init__(self, chunksize, data):
        """

        """
        self.chunksize = chunksize
        self.size = pow(chunksize, 2)
        # a cell you know nothing about could contain anything from the set of all pieces
        # call this the 'empty set'
        self.empty_set = set(int2piece(a) for a in range(1, self.size+1))
        # replace empty sets with the 'empty set' (copied!!)
        self.data = [list(map(lambda x: x if len(x)>0 else self.empty_set.copy(), row)) for row in data]

    def get(self, col_index, row_index):
        """Retrieve a cell
        """
        return self.data[row_index][col_index]

    def set(self, col_index, row_index, value: set):
        """Set a cell's value
        """
        self.data[row_index][col_index] = value

    def clear(self, row_index, col_index, value):
        """'Clear' a cell by loading the 'empty set' (i.e. we don't know what's in it)
        """
        self.data[row_index][col_index] = self.empty_set

    def validate_row(self, row_index):
        """
        Is a row possible?
        Attempt 1: Does any 'certain' piece occur more than once?

        """
        f_tally = set()
        for c in range(0, self.size):
            f = self.data[row_index][c]
            # chunk already has digit f
            if len(f) == 1:
                # get only item in set
                (piece,) = f # tuple unpack only item in set
                if piece in f_tally:
                    return False
                f_tally.add(piece)
        return True

    def validate_col(self, col_index):
        """
        Is a col possible?
        Attempt 1: Does any 'certain' piece occur more than once?

        """
        f_tally = set()
        for r in range(0, self.size):
            f = self.data[r][col_index]
            # chunk already has digit f
            if len(f) == 1:
                # get only item in set
                (piece,) = f # tuple unpack only item in set
                if piece in f_tally:
                    return False
                f_tally.add(piece)
        return True

    def get_chunk_coords(self, col_index, row_index):
        return col_index // self.chunksize, row_index // self.chunksize

    def validate_chunk_for_cell(self, col_index, row_index):
        """Validate the chunk containing a give cell
        """
        cc, cr = self.get_chunk_coords(col_index, row_index)
        return self.validate_chunk(cc, cr)

    def is_solved(self):
        """Do all cell contain exactly one possibility?
        """
        maximax = max(map(lambda row: max(map(len, row)), self.data))

        if maximax == 1:
            return True

        return False

    def validate_all_chunks(self):
        """
        Rough chunk check
        """
        result = True

        for chunk_row in range(0, self.chunksize):
            for chunk_col in range(0, self.chunksize):
                result &= self.validate_chunk(chunk_row, chunk_col)

        return result

    def get_chunk_set_for_cell(self, col_index, row_index):
        cc, cr = self.get_chunk_coords(col_index, row_index)
        f_tally = set()
        for r in range(cr * self.chunksize, (cr + 1) * self.chunksize):
            for c in range(cc * self.chunksize, (cc + 1) * self.chunksize):
                f = self.data[r][c]
                f_tally.update(f)
        return f_tally

    def validate_chunk(self, cr, cc):
        """
        extract the chunksize*chunksize chunk at chunkrow cr and chunkcol cc
        and determine if it meets the sudoko constraints for a chunk

        """
        f_tally = set()
        for r in range(cr * self.chunksize, (cr + 1) * self.chunksize):
            for c in range(cc * self.chunksize, (cc + 1) * self.chunksize):
                f = self.data[r][c]
                # chunk already has digit f
                if len(f) == 1:
                    # get only item in set
                    (piece,) = f # tuple unpack only item in set
                    if piece in f_tally:
                        return False
                    f_tally.add(piece)
        return True

    def reduce_cell(self, col_index, row_index):
        """
        Attempts to resolve the cell, row and column contraints
        and remove possibilities from a cell
        """
        this_cell = self.get(col_index, row_index)
        #d(this_cell)
        if len(this_cell) == 1:
            # cell needs no further reduction
            return 1
        # get chunk set
        cc, cr = self.get_chunk_coords(col_index, row_index)
        #d(col_index, row_index, cc, cr)
        f_tally = set()
        # find all certainties in this chunk
        for r in range(cr * self.chunksize, (cr + 1) * self.chunksize):
            for c in range(cc * self.chunksize, (cc + 1) * self.chunksize):
                f = self.get(c, r)
                if len(f) == 1:
                    f_tally.update(f)
        # find all certainties in this row
        for c in range(0, self.size):
            f = self.get(c, row_index)
            if len(f) == 1:
                f_tally.update(f)
        # find all certainties in this col
        for r in range(0, self.size):
            f = self.get(col_index, r)
            if len(f) == 1:
                f_tally.update(f)
        # remove 
        this_cell.difference_update(f_tally)
        if len(this_cell) == 0:
            return IMPOSSIBLE
        # return a count of remaining possibilities (if it's 1 we're getting closer)
        self.set(col_index, row_index, this_cell.copy())
        return len(this_cell)

    def find_first_unsolved_cell(self):
        for r in range(0, self.size):
            for c in range(0, self.size):
                f = self.get(c, r)
                if len(f) > 1:
                    return c,r


def solve(puzzle):
    """
    algorithm v1:

    each cell is a sequence of possible pieces
    repeat
        iterate through each cell where len(possibilities) > 1
            test each possibilities against row, cell and chunk removing any that fail
            if max(len(possibilities)) == 1
                return solve
            else if no changes this pass
                return unsolvable
    """
    # e.g. 9 x 9 = 81 = 1 possibility for each row
    win_score = pow(puzzle.size, 2)

    # start with total sum of possibilities
    last_run = sum(map(lambda row: sum(map(len, row)), puzzle.data))

    # converge based on certainties
    while True:
        this_run = 0
        for c in range(0, puzzle.size):
            for r in range(0, puzzle.size):
                result = puzzle.reduce_cell(c, r)
                if result == IMPOSSIBLE:
                    return IMPOSSIBLE, puzzle
                this_run += result
        if last_run == this_run:
            # we can't converge any more
            d( f"Converged to {this_run}" )
            break
        last_run = this_run

    if this_run == win_score:
        d( f"Win {this_run}" )
        return this_run, puzzle
    if this_run < win_score:
        d(format_puzzle(puzzle))
        raise AlgorithmException(f"this_run {this_run} is lower than minimum possible of {win_score}")
    else:
        # start searching
        un_c, un_r = puzzle.find_first_unsolved_cell()
        f = puzzle.get(un_c, un_r)
        for poss in f:
            d(f"Forking {un_c},{un_r},{poss}")
            new_puzzle = copy.deepcopy(puzzle)
            new_puzzle.set(un_c, un_r, set([poss]))
            this_run, new_puzzle = solve(new_puzzle)
            if this_run == win_score:
                return this_run, new_puzzle

        return this_run, puzzle


def format_puzzle(puzzle):
    """Renders a puzzle including possibility sets
    """
    return "\n".join(" ".join( "{" + ",".join(col) + "}" for col in row) for row in puzzle.data)

#    op = ""
#    for row in puzzle.data:
#        for col in row:
#            op += ",".join(col) + " "
#        op += "\n"
#    return op

def read_puzzle(inp):
    """
        Take these lines from stdin containing whitespace separated
        'pieces' or 'blanks'
            8 _ _  _ 9 _  2 5 _
            5 _ _  _ 7 _  6 _ 1
            _ _ _  8 _ _  _ 9 4

            _ 7 5  9 4 _  _ _ _
            6 4 _  7 _ 8  _ _ _
            _ _ _  _ 2 6  4 7 _

            9 2 _  _ _ 4  _ _ _
            7 _ 8  _ 1 _  _ _ 2
            _ 5 6  _ 8 _  _ _ 9

        ...and turn into a puzzle.

        Treats all pieces as strings as the fact they're digits is
        irrelevant to the puzzle
    """
    size = 0
    empty_set = set() # initialise to enter set of 'pieces'
    rows = []
    for rowc, line in enumerate(line for line in inp):

        # split on any number of spaces
        chunks = split(r"\s+", line.strip())

        # discard empty cells (they should be explicitly denoted with a non-numerical char
        chunks = filter(lambda x: x!='', chunks)
        # use "" as empty cell placeholder
        chunks = list(map(lambda x: x.upper() if x not in BLANKS else "", chunks))

        if len(chunks) == 0:
            # skip blank lines
            continue

        # initialise size of puzzle
        if size==0:
            size = len(chunks)
            # sudoku's need to be squares of squares
            # https://en.wikipedia.org/wiki/Glossary_of_Sudoku#Variants_by_size
            if size not in (4,9):
                # TODO support greater than decimal variants (e.g. [0-9A-Z])
                raise FormatException("Square size not a square number!")
        else:
            if len(chunks) != size:
                raise FormatException(f"Row {rowc} doesn't match first row size")


        # convert pieces to sequences of possibilities
        # BLANKS are initially an empty set (but later we'll expand)
        chunks = list(map(lambda x: set([x,]) if x != "" else set(), chunks))

        rows.append(chunks)

    return int(sqrt(size)),rows

def int2piece(i):
    """Converts an int between 1 and chunksize^2 to a alphanum, human-readable piece
    e.g.
        1 -> "1"
        10 -> "A"
    Note this is NOT hexadecimal
    """
    if i > 0 and i <= 9:
        # 0 - 9
        return chr(48+i)
    elif i > 9 and i <= 35:
        # A - Z
        return chr(65+i-10)
    else:
        raise FormatException(
            "I don't support puzzles with more than 35 symbols (so in practice 25x25)"
        )

def run(inp):
    """Placeholder entrypoint
    """
    chunksize, raw_puzzle = read_puzzle(inp)
    puzzle = Puzzle(chunksize, raw_puzzle)
    score, puzzle = solve(puzzle)
    print(format_puzzle(puzzle))

if __name__ == "__main__":
    run(sys.stdin)
