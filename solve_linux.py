#!/usr/bin/env python3
import sys
from cgp_solver import get_expression
import minisat


def default_usage():
    # The argument must reference an instance file and the second
    print("Usage:", sys.argv[0], "INSTANCE_FILE", file=sys.stderr)
    exit(1)


def get_row(grid, i):
    return grid[i]


def get_column(grid, j):
    out = []
    for i in range(len(grid)):
        out.append(grid[i][j])
    return out


def get_left_diag(grid, i, j):
    out = []
    for add in range(-len(grid), len(grid)):
        if i+add >= 0 and i + add < len(grid) and j+add >= 0 and j+add < len(grid):
            out.append(grid[i+add][j+add])
    return out


def get_right_diag(grid, i, j):
    out = []
    for add in range(-len(grid), len(grid)):
        if i + add >= 0 and i + add < len(grid) and j - add >= 0 and j - add < len(grid):
            out.append(grid[i + add][j - add])
    return out


def read_instance(instance_file):
    file = open(instance_file)
    size = int(file.readline().split(' ')[0])
    queens = []
    line = file.readline()
    while line:
        queens.append((int(line.split(' ')[0]), int(line.split(' ')[1])))
        line = file.readline()
    return size, queens


if __name__ == "__main__":
    if len(sys.argv) != 2:
        default_usage()

    size, queens = read_instance(sys.argv[1])
    n_rows = n_columns = size
    expression = get_expression(size, queens)
    nb_vars = n_rows * n_columns
    solution = minisat.minisat(nb_vars, [clause.minisat_str() for clause in expression])

    if solution is None:
        print("The problem is unfeasible")
        exit(0)
    grid = [[0 for _ in range(size)] for _ in range(size)]
    for s in solution:
        grid[(s-1)//size][(s-1)%size] = 1

    clean = True
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if sum(get_row(grid, i)) != 1:
                clean = False
                print("FAIL. Row {0} is not different.".format(i))
            if sum(get_column(grid, j)) != 1:
                clean = False
                print("FAIL. Column {0} is not different.".format(i))
            if sum(get_left_diag(grid, i, j)) != 1:
                clean = False
                print("FAIL. Left diagonal passing through cell ({0},{1}) is not different.".format(i, j))
            if sum(get_right_diag(grid, i, j)) != 1:
                clean = False
                print("FAIL. Right diagonal passing through cell ({0},{1}) is not different.".format(i, j))
    for queen in queens:
        if grid[queen[0]][queen[1]] != 1:
            clean = False
            print("FAIL. There is no queen in case ({0},{1}) as required".format(queen[0], queen[1]))
    if clean:
        print("SOLVED")
        for row in grid:
            print(row)
