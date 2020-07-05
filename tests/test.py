import unittest
from unittest import TestCase

import sudoku as sdku


def try_int_or_None(val):
    try:
        return int(val)
    except:
        return None


def read_puzzle_from_string(puzzle_str):
    lines = puzzle_str.split('\n')
    puzzle = []
    for line in lines:
        values = [try_int_or_None(value) for value in line.strip().split()]
        puzzle.append(values)
    return puzzle


def read_puzzle(path):
    with open(path, 'r') as f:
        data = f.read().strip()
    return read_puzzle_from_string(data)


class TestSudoku(TestCase):
    def test_read_from_string(self):
        puzzle_str = """
        . . 7 . 2 4 . 3 8
        . . . 6 5 9 . 2 4
        2 4 . . . . 5 . .
        9 . . 7 . 1 . . .
        . . 1 . 8 . 9 . .
        . . . 5 . 6 . . 3
        . . 8 . . . . 1 7
        1 2 . 8 6 7 . . .
        7 5 . 2 1 . 4 . .
        """
        puzzle = read_puzzle_from_string(puzzle_str)

    def test_read_puzzle(self):
        path = 'tests/data/001.txt'
        puzzle = read_puzzle(path)
        first_row_len = len(puzzle[0])
        self.assertTrue(all(len(p) == first_row_len for p in puzzle))

    def test_reads_001_correctly(self):
        path = 'tests/data/001.txt'
        puzzle = read_puzzle(path)
        expected = [
            [ None, None,    7,    None,    2,    4,    None,    3,    8],
            [ None, None, None,       6,    5,    9,    None,    2,    4],
            [    2,    4, None,    None, None, None,       5, None, None],

            [    9, None, None,       7, None,    1,    None, None, None],
            [ None, None,    1,    None,    8, None,       9, None, None],
            [ None, None, None,       5, None,    6,    None, None,    3],

            [ None, None,    8,    None, None, None,    None,    1,    7],
            [    1,    2, None,       8,    6,    7,    None, None, None],
            [    7,    5, None,       2,    1, None,       4, None, None],
        ]
        self.assertEqual(puzzle, expected)
        puzzle[4][4] = 1
        self.assertNotEqual(puzzle, expected)

    def test_get_zone(self):
        self.assertEqual(sdku.get_zone(0,0), (0,0))
        self.assertEqual(sdku.get_zone(0,1), (0,0))
        self.assertEqual(sdku.get_zone(1,0), (0,0))
        self.assertEqual(sdku.get_zone(1,1), (0,0))

    def test_solve_easy_1(self):
        path = 'tests/data/easy_001.txt'
        puzzle = read_puzzle(path)
        solved = sdku.solve(puzzle)
        self.assertTrue(sdku.is_solved(solved))

    def test_solve_easy_1a(self):
        path = 'tests/data/easy_001-a.txt'
        puzzle = read_puzzle(path)
        solved = sdku.solve(puzzle)
        self.assertTrue(sdku.is_solved(solved))

    def test_backtracking(self):
        path = 'tests/data/hard_001.txt'
        puzzle = read_puzzle(path)
        with_guesses = sdku.solve_easy(puzzle)
        solved = sdku.solve_by_backtracking(with_guesses)
        self.assertTrue(sdku.is_solved(solved))

    def test_solve_easy_001(self):
        path = 'tests/data/001.txt'
        puzzle = read_puzzle(path)
        solved = sdku.solve(puzzle)
        self.assertTrue(sdku.is_solved(solved))

    def test_solve_hard_001(self):
        path = 'tests/data/hard_001.txt'
        puzzle = read_puzzle(path)
        solved = sdku.solve(puzzle)
        self.assertTrue(sdku.is_solved(solved))

    def test_solve_hard_002(self):
        path = 'tests/data/hard_002.txt'
        puzzle = read_puzzle(path)
        solved = sdku.solve(puzzle)
        sdku.display_puzzle(solved)
        self.assertTrue(sdku.is_solved(solved))

if __name__ == '__main__':
    unittest.main()
