from clause import *

"""
For the queen problem, the only code you have to do is in this file.

You should replace

# your code here

by a code generating a list of clauses modeling the queen problem
for the input file.

You should build clauses using the Clause class defined in clause.py

Read the comment on top of clause.py to see how this works.
"""


def get_expression(size, queens=None):
    expression = []
    for i in range(size):
        min_col, min_row = Clause(size), Clause(size)
        for j in range(size):
            min_col.add_positive(i,j)
            min_row.add_positive(j,i)
            for k in range(size):
                if k != i:
                    max_row = Clause(size)
                    max_row.add_negative(i,j)
                    max_row.add_negative(k,j)
                    expression.append(max_row)
                if k != j:
                    max_col = Clause(size)
                    max_col.add_negative(i, j)
                    max_col.add_negative(i, k)
                    expression.append(max_col)
            for d in range(1,size):
                if i+d < size and j + d < size:
                    max_right_down_diag = Clause(size)
                    max_right_down_diag.add_negative(i,j)
                    max_right_down_diag.add_negative(i+d,j+d)
                    expression.append(max_right_down_diag)
                if i-d >= 0 and j-d >= 0:
                    max_left_up_diag = Clause(size)
                    max_left_up_diag.add_negative(i, j)
                    max_left_up_diag.add_negative(i - d, j - d)
                    expression.append(max_left_up_diag)
                if i+d < size and j - d >= 0:
                    max_left_down_diag = Clause(size)
                    max_left_down_diag.add_negative(i,j)
                    max_left_down_diag.add_negative(i+d,j-d)
                    expression.append(max_left_down_diag)
                if i-d >= 0 and j + d < size:
                    max_right_up_diag = Clause(size)
                    max_right_up_diag.add_negative(i,j)
                    max_right_up_diag.add_negative(i-d,j+d)
                    expression.append(max_right_up_diag)
        expression += [min_col,min_row]
    for queen in queens:
        q = Clause(size)
        q.add_positive(queen[0],queen[1])
        expression.append(q)

    return expression


if __name__ == '__main__':
    expression = get_expression(3)
    for clause in expression:
        print(clause)
