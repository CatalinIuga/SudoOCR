import z3


def solve_sudoku(table):
    z3_table = [[z3.Int(f"z3_table_{i}_{j}")
                 for j in range(9)] for i in range(9)]

    constraints = []

    for i in range(9):
        for j in range(9):
            if table[i][j] != 0:
                constraints.append(z3_table[i][j] == table[i][j])

    for i in range(9):
        constraints.append(z3.Distinct(z3_table[i]))

    for j in range(9):
        constraints.append(z3.Distinct([z3_table[i][j] for i in range(9)]))

    for i in range(3):
        for j in range(3):
            constraints.append(z3.Distinct(
                [z3_table[3*i + k][3*j + l] for k in range(3) for l in range(3)]))

    for i in range(9):
        for j in range(9):
            constraints.append(
                z3.And(z3_table[i][j] >= 1, z3_table[i][j] <= 9))

    s = z3.Solver()
    s.add(constraints)
    if s.check() == z3.sat:
        m = s.model()
        return [[m[z3_table[i][j]].as_long() for j in range(9)] for i in range(9)]
    else:
        return None
