"""
    Glossary:
        cell - a space on the puzzle board
        piece - a number (or alphanum or other symbol in 16+ size boards)
        chunksize - the 'fractal' unit of this board, typically 3 (9x9 game) or 4 (16x16)
        row - one chunksize^2 row from left to right, 0 indexed
        col - one chunksize^2 column from top to bottom, 0 indexed
        zone - the chunksize x chunksize square collection of cells, 0 indexed TL to BR

    algorithm v1:

    each cell is a sequence of possible pieces
    repeat
        iterate through each cell where len(possibilities) > 1
            test each possibilities against row, cell and zone removing any that fail
            if max(len(possibilities)) == 1
                return solve
            else if no changes this pass
                return unsolvable
"""

import sys
from re import split
import logging
from math import sqrt

BLANKS = ('_', '-', '*', '.')

logging.basicConfig(level=logging.DEBUG)

class FormatException(Exception):
    """Error relating to input file format
    """

def d(str):
    logging.debug(str)

class Puzzle():
    """
        rows -> 0 indexed starting from top
        cols -> 0 indexed starting from left
    """
    def __init__(self, chunksize, data):
        self.chunksize = chunksize
        self.size = pow(chunksize, 2)
        self.data = data

    def get(self, col_index, row_index):
        """Retrieve a cell
        """
        return self.data[row_index][col_index]

    def set(self, col_index, row_index, value: set):
        """Set a cell's value
        """
        self.data[row_index][col_index] = value

    def clear(self, row_index, col_index, value):
        pass

    def validate_row(self, row_index):
        pass

    def validate_col(self, col_index):
        pass

    def validate_zone_for_cell(self, col_index, row_index):
        """Validate the zone containing a give cell
        """
        cc = col_index // self.chunksize
        cr = row_index // self.chunksize
        return self.validate_zone(cc, cr)

    def is_solved(self):
        """Do all cell contain exactly one possibility?
        """
        maximax = max(map(lambda row: max(map(len, row)), self.data))

        if maximax == 1:
            return True

        return False

    def validate_all_zones(self):
        """
        Rough zone check
        """
        result = True

        for chunk_row in range(0, self.chunksize):
            for chunk_col in range(0, self.chunksize):
                result &= self.validate_zone(chunk_row, chunk_col)

        return result

    def validate_zone(self, cr, cc):
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

def solve(puzzle):
    pass

def format_puzzle(puzzle):
    return "\n".join(" ".join( "{" + ",".join(col) + "}" for col in row) for row in puzzle.data)

    op = ""
    for row in puzzle.data:
        for col in row:
            op += ",".join(col) + " "
        op += "\n"
    return op

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

        # by now we know puzzle size, so computer the piece set
        empty_set = set(int2piece(a) for a in range(1, size+1))

        # convert pieces to sequences of possibilities
        # BLANKS are initially a list of all pieces
        chunks = list(map(lambda x: set([x,]) if x != "" else empty_set, chunks))

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
    d(puzzle.data)
    r = puzzle.validate_all_zones()
    d(r)

if __name__ == "__main__":
    run(sys.stdin)
    #print(r)
