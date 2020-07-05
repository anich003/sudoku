"""
A puzzle is a list of lists where the list elements are:
    an int representing a fixed number
    a set of ints representing the possible values given the rest of the puzzle

Solving a puzzle happens in two phases:
    1. Solve "easy" cells: Iteratively pass through the puzzle, fixing as
       many unknown cells, using the currently known cells. Since each new
       determined cells changes the puzzle, this is run many times until
       no new cells can be determined from the current puzzle state.
    2. Solve "hard" cells with tree search

def solve(puzzle):
    with_guesses = solve_easy(puzzle)
    solved = solve_hard(with_guesses)
    return solved


solve_easy: List[List[Optional[int]]] -> List[List[Either[int, Set[int]]]]
solve_hard: List[List[Either[int, Set[int]]]] -> List[List[int]]

     solve: List[List[Optional[int]]] -> List[List[int]]

"""
import copy
import math
from typing import List, Union, Optional, Set


def is_row_valid(puzzle, i):
    values = [v for v in puzzle[i] if type(v) == int]
    return len(set(values)) == len(values)


def is_col_valid(puzzle, i):
    values = [row[i] for row in puzzle if type(row[i]) == int]
    return len(set(values)) == len(values)


def is_zone_valid(puzzle, row, col):
    values = get_zone_values(puzzle, row, col)
    return len(set(values)) == len(values)


def are_zones_valid(puzzle):
    n = len(puzzle[0])
    zones = {}
    for row in range(n):
        for col in range(n):
            zone = get_zone(row, col)
            list_ = zones.get(zone, [])
            list_.append(puzzle[row][col])
            zones[zone] = list_
            
    for zone, list_ in zones.items():
        values = [v for v in list_ if type(v) == int]
        if len(set(values)) != len(values):
            return False
    return True
        


def is_valid(puzzle):
    n = len(puzzle[0])
    for i in range(n):
        if not is_row_valid(puzzle, i) or not is_col_valid(puzzle, i):
            return False
    if not are_zones_valid(puzzle):
        return False
    return True
        

def is_solved(puzzle):
    return all(type(value) == int
               for row in puzzle
               for value in row)


def get_zone(row, col) -> (int, int):
    return (row//3,col//3)


def is_int(val):
    return type(val) == int


def is_guess(val):
    return type(val) == set


def get_zone_values(puzzle, row, col, predicate=is_int):
    zone = get_zone(row, col)
    values = []
    for r in range(9):
        for c in range(9):
            if get_zone(r,c) == zone:
                if predicate(puzzle[r][c]):
                    values.append(puzzle[r][c])
    return values


def collect_guesses(vals) -> set:
    if len(vals) == 0:
        return set()
    return set.union(*vals)


def refine_guesses(puzzle, row, col) -> Set[int]:
    value_set = puzzle[row][col]

    if value_set is None:
        value_set = set(range(1, 9+1))

    # Compare against row, col, and zone values
    row_values = set(v for v in puzzle[row] if type(v) == int)
    col_values = set(row[col] for row in puzzle if type(row[col]) == int)
    zone_values = set(v for v in get_zone_values(puzzle, row, col))

    guesses = value_set - (row_values | col_values | zone_values)

    # Compare against row, col and zone guesses
    # row_guesses = collect_guesses([el for el in puzzle[row] if is_guess(el)])
    #
    # col_guesses = collect_guesses([row[col] for row in puzzle if is_guess(row[col])])
    # zone_guesses = collect_guesses([v for v in get_zone_values(puzzle, row, col, is_guess)])
    #
    # guesses = guesses - row_guesses if len(guesses - row_guesses) == 1 else guesses
    # guesses = guesses - col_guesses
    # guesses = guesses - zone_guesses

    return guesses


def get_children(puzzle):
    n = len(puzzle[0])
    for row in range(n):
        for col in range(n):
            entry = puzzle[row][col]
            if type(entry) == set:
                for guess in entry:
                    new_child = copy.deepcopy(puzzle)
                    new_child[row][col] = guess
                    yield new_child


def display_puzzle(puzzle):
    for row in puzzle:
        for value in row:
            print(f'{value if value else "."}', end=' ')
        print()
    print('\n')


def solve_easy(puzzle: List[List[Optional[int]]]) -> List[List[Union[int, Set[int]]]]:
    new_puzzle = copy.deepcopy(puzzle)
    n = len(new_puzzle[0])
    # Iteratively reduce each set of guesses
    keep_going = True
    while keep_going:
        keep_going = False

        for row in range(n):
            for col in range(n):
                entry = new_puzzle[row][col]

                if entry is None:
                    new_entry = refine_guesses(new_puzzle, row, col)
                    keep_going=True
                    new_puzzle[row][col] = new_entry

                elif type(entry) == set:
                    new_entry = refine_guesses(new_puzzle, row, col)
                    if len(new_entry) == 1:
                        new_entry = new_entry.pop()
                        keep_going = True
                    new_puzzle[row][col] = new_entry
    return new_puzzle

def solve_by_backtracking(puzzle):
    if is_solved(puzzle):
        return puzzle

    if not is_valid(puzzle):
        return None

    for r in range(9):
        for c in range(9):
            if is_int(puzzle[r][c]):
                continue
            for guess in puzzle[r][c]:
                new_puzzle = copy.deepcopy(puzzle)
                new_puzzle[r][c] = guess
                solution = solve_by_backtracking(new_puzzle)
                if solution:
                    return solution
            return None


def solve_hard(puzzle: List[List[Union[int, Set[int]]]]) -> List[List[int]]:
    if is_solved(puzzle):
        return puzzle

    candidate_puzzles = [puzzle]

    # DFS for solution
    while candidate_puzzles:
        print(len(candidate_puzzles))
        current_puzzle = candidate_puzzles.pop()
        current_puzzle = solve_easy(current_puzzle)
        if not is_valid(current_puzzle):
            continue

        if is_solved(current_puzzle):
            return current_puzzle

        for candidate in get_children(current_puzzle):
            candidate_puzzles.append(candidate)

def solve(puzzle):
    with_guesses = solve_easy(puzzle)
    solved = solve_by_backtracking(with_guesses)
    return solved


if __name__ == '__main__':
    from tests.test import read_puzzle
    path = 'tests/data/001.txt'
    puzzle = read_puzzle(path)
