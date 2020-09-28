from sudokuloco import solver
import pytest
import logging

#def test_foo(caplog):
#    caplog.set_level(logging.DEBUG)
#    pass

def test_read_puzzle():
    """Test we can read data from a valid puzzle file"""
    with open('tests/valid_incomplete_9.txt') as inp:
        chunksize, puzzle = solver.read_puzzle(inp)
        assert chunksize == 3
        assert len(puzzle) == 9
        assert len(puzzle[0]) == 9

@pytest.mark.xfail(raises=solver.FormatException)
def test_read_malformed_puzzle():
    """Ensure puzzle file with an error doens't work"""
    with open('tests/missing_row_9.txt') as inp:
        solver.read_puzzle(inp)

def get_valid_incomplete():
    """Utility to open a valid puzzle file"""
    with open('tests/valid_incomplete_9.txt') as inp:
        return solver.read_puzzle(inp)

def get_valid_complete():
    """Utility to open a valid complete puzzle file"""
    with open('tests/valid_complete_9.txt') as inp:
        return solver.read_puzzle(inp)

def get_easy_incomplete():
    """Utility to open a valid incomplete puzzle file that has one empty cell"""
    with open('tests/easy_incomplete_9.txt') as inp:
        return solver.read_puzzle(inp)

def get_invalid_incomplete():
    """Utility to open an invalid incomplete puzzle file"""
    with open('tests/invalid_incomplete_9.txt') as inp:
        return solver.read_puzzle(inp)

def test_puzzle_obj():
    """Test a puzzle obj wraps the raw_data
    nicely and that all the methods work ok
    according to:

            8 _ _  _ 9 _  2 5 _
            5 _ _  _ 7 _  6 _ 1
            _ _ _  8 _ _  _ 9 4

            _ 7 5  9 4 _  _ _ _
            6 4 _  7 _ 8  _ _ _
            _ _ _  _ 2 6  4 7 _

            9 2 _  _ _ 4  _ _ _
            7 _ 8  _ 1 _  _ _ 2
            _ 5 6  _ 8 _  _ _ 9

    """
    chunksize, raw_puzzle = get_valid_incomplete()
    puzzle = solver.Puzzle(chunksize, raw_puzzle)
    assert puzzle.get(0,0) == set(["8"])
    assert puzzle.get(1,0) == set(["1","2","3","4","5","6","7","8","9"])

def test_is_complete():
    chunksize, raw_puzzle = get_valid_complete()
    puzzle = solver.Puzzle(chunksize, raw_puzzle)
    assert puzzle.is_solved() == True
    chunksize, raw_puzzle = get_valid_incomplete()
    puzzle = solver.Puzzle(chunksize, raw_puzzle)
    assert puzzle.is_solved() == False


def test_validate_column():
    """
    Does a known valid single incomplete column validate?
    """
    chunksize, raw_puzzle = get_valid_incomplete()
    puzzle = solver.Puzzle(chunksize, raw_puzzle)
    assert puzzle.validate_col(1) == True
    chunksize, raw_puzzle = get_valid_complete()
    puzzle = solver.Puzzle(chunksize, raw_puzzle)
    assert puzzle.validate_col(1) == True
    chunksize, raw_puzzle = get_invalid_incomplete()
    puzzle = solver.Puzzle(chunksize, raw_puzzle)
    assert puzzle.validate_col(1) == False


def test_validate_row():
    """
    Does a known valid single incomplete row validate?
    """
    chunksize, raw_puzzle = get_valid_incomplete()
    puzzle = solver.Puzzle(chunksize, raw_puzzle)
    assert puzzle.validate_row(0) == True
    chunksize, raw_puzzle = get_valid_complete()
    puzzle = solver.Puzzle(chunksize, raw_puzzle)
    assert puzzle.validate_row(0) == True
    chunksize, raw_puzzle = get_invalid_incomplete()
    puzzle = solver.Puzzle(chunksize, raw_puzzle)
    assert puzzle.validate_row(0) == False

def test_validate_chunk():
    """
    Does a known valid single incomplete chunk validate?
    """
    chunksize, raw_puzzle = get_valid_incomplete()
    puzzle = solver.Puzzle(chunksize, raw_puzzle)
    assert puzzle.validate_chunk(0, 0) == True
    assert puzzle.validate_chunk(1, 1) == True
    assert puzzle.validate_chunk(2, 2) == True
    chunksize, raw_puzzle = get_valid_complete()
    puzzle = solver.Puzzle(chunksize, raw_puzzle)
    assert puzzle.validate_chunk(0, 0) == True
    assert puzzle.validate_chunk(1, 1) == True
    assert puzzle.validate_chunk(2, 2) == True

def test_validate_chunk_by_cell_index():
    """
    Does a known valid single incomplete chunk validate?
    """
    chunksize, raw_puzzle = get_valid_incomplete()
    puzzle = solver.Puzzle(chunksize, raw_puzzle)
    for ccc in range(0, 9):
        assert puzzle.validate_chunk_for_cell(ccc, ccc) == True
    chunksize, raw_puzzle = get_invalid_incomplete()
    puzzle = solver.Puzzle(chunksize, raw_puzzle)
    for ccc in range(0, 3):
        assert puzzle.validate_chunk_for_cell(ccc, ccc) == False
    for ccc in range(3, 9):
        assert puzzle.validate_chunk_for_cell(ccc, ccc) == True

def test_validate_all_chunks():
    """
    Does a known valid puizzle validate all chunks?
    """
    chunksize, raw_puzzle = get_valid_incomplete()
    puzzle = solver.Puzzle(chunksize, raw_puzzle)
    assert puzzle.validate_all_chunks() == True
    chunksize, raw_puzzle = get_valid_complete()
    puzzle = solver.Puzzle(chunksize, raw_puzzle)
    assert puzzle.validate_all_chunks() == True

def test_print_puzzle():
    chunksize, raw_puzzle = get_valid_complete()
    puzzle = solver.Puzzle(chunksize, raw_puzzle)
    op = solver.format_puzzle(puzzle)
    assert op == """{5} {3} {4} {6} {7} {8} {9} {1} {2}
{6} {7} {2} {1} {9} {5} {3} {4} {8}
{1} {9} {8} {3} {4} {2} {5} {6} {7}
{8} {5} {9} {7} {6} {1} {4} {2} {3}
{4} {2} {6} {8} {5} {3} {7} {9} {1}
{7} {1} {3} {9} {2} {4} {8} {5} {6}
{9} {6} {1} {5} {3} {7} {2} {8} {4}
{2} {8} {7} {4} {1} {9} {6} {3} {5}
{3} {4} {5} {2} {8} {6} {1} {7} {9}"""
    print()
    print(op)
    chunksize, raw_puzzle = get_valid_incomplete()
    puzzle = solver.Puzzle(chunksize, raw_puzzle)
    op = solver.format_puzzle(puzzle)
    print()
    print(op)

def test_reduce():
    chunksize, raw_puzzle = get_easy_incomplete()
    puzzle = solver.Puzzle(chunksize, raw_puzzle)
    assert puzzle.get(1,0) == set(["1","2","3","4","5","6","7","8","9"])
    puzzle.reduce_cell(1,0)
    assert puzzle.get(1,0) == set(["3"])

def test_solve():
    chunksize, raw_puzzle = get_valid_incomplete()
    puzzle = solver.Puzzle(chunksize, raw_puzzle)
    op = solver.format_puzzle(puzzle)
    print()
    print(op)
    score, puzzle = solver.solve(puzzle)
    op = solver.format_puzzle(puzzle)
    print()
    print(op)
    assert True
    


def test_int_2_piece():
    assert solver.int2piece(1) == "1"
    assert solver.int2piece(9) == "9"
    assert solver.int2piece(10) == "A"
    assert solver.int2piece(35) == "Z"
