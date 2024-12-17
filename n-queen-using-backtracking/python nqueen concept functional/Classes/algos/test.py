from pyrsistent import pvector

# Constants
N = 8


def my_reduce(function, iter, accumulator):
    if not iter:
        return accumulator

    new_accumulator = function(iter[0], accumulator)

    return my_reduce(function, iter[1:], new_accumulator)


def my_map(function, iter):
    return my_reduce(
        lambda element, accumulator: accumulator.append(function(element)),
        iter,
        pvector(),
    )

def my_filter(function, iter):
    return my_reduce(
        lambda element, accumulator: (
            accumulator.append(element) if function(element) else accumulator
        ),
        iter,
        pvector(),
    )


def my_compose(f, g):
    return lambda *args: f(g(*args))


def printSolution(board, i=0, j=0, N=None):

    if N is None:
        N = len(board)

    if i == N:
        return

    print(board[i][j], end=" ")

    if j == N - 1:
        print()
        printSolution(board, i + 1, 0, N)
    else:
        printSolution(board, i, j + 1, N)


def check_row_for_conflict_with_map(board, row, col):
    return any(my_map(lambda i: board[row][i] == 1, range(col)))


def check_upper_diag_for_conflict_with_map(board, row, col):
    return any(
        my_map(
            lambda i_j: board[i_j[0]][i_j[1]] == 1,
            pvector(zip(range(row, -1, -1), range(col, -1, -1))),
        )
    )


def check_lower_diag_for_conflict_with_map(board, row, col):
    return any(
        my_map(
            lambda i_j: board[i_j[0]][i_j[1]] == 1,
            pvector(zip(range(row, N), range(col, -1, -1))),
        )
    )


def lambda_test(x):
    return x


def check_all_conflicts_composed(board, row, col):
    return my_compose(
        lambda x: lambda_test(x)
        or check_lower_diag_for_conflict_with_map(board, row, col),
        my_compose(
            lambda x: x or check_upper_diag_for_conflict_with_map(board, row, col),
            check_row_for_conflict_with_map,
        ),
    )(board, row, col)


def isSafe(board, row, col):

    if check_all_conflicts_composed(board, row, col):
        return False

    return True


def solveNQUtil(board, col):
    if col >= N:
        return True

    safe_rows = my_filter(lambda row: isSafe(board, row, col), range(N))
    print(safe_rows)

    def tryPlaceQueen(row):

        board[row][col] = 1

        if solveNQUtil(board, col + 1):
            return True
        board[row][col] = 0
        return False

    return my_reduce(lambda row, acc: acc or tryPlaceQueen(row), safe_rows, False)


def solveNQ():
    board = [[0] * N for _ in range(N)]

    if not solveNQUtil(board, 0):
        print("Solution does not exist")
        return False

    printSolution(board)
    return True


solveNQ()




# # Adjust functions for immutable data structures
# def check_row_for_conflict_with_map(board, row, col):
#     return any(my_map(lambda i: board[row][i] == 1, range(col)))

# def check_upper_diag_for_conflict_with_map(board, row, col):
#     return any(
#         my_map(
#             lambda i_j: board[i_j[0]][i_j[1]] == 1,
#             list(zip(range(row, -1, -1), range(col, -1, -1))),
#         )
#     )

# def check_lower_diag_for_conflict_with_map(board, row, col):
#     return any(
#         my_map(
#             lambda i_j: board[i_j[0]][i_j[1]] == 1,
#             list(zip(range(row, N), range(col, -1, -1))),
#         )
#     )

# def lambda_test(x):
#     return x

# def check_all_conflicts_composed(board, row, col):
#     return my_compose(
#         lambda x: lambda_test(x)
#         or check_lower_diag_for_conflict_with_map(board, row, col),
#         my_compose(
#             lambda x: x or check_upper_diag_for_conflict_with_map(board, row, col),
#             check_row_for_conflict_with_map,
#         ),
#     )(board, row, col)

# def isSafe(board, row, col):
#     if check_all_conflicts_composed(board, row, col):
#         return False
#     return True

# # Solve N Queens using pyrsistent's immutable structures
# def solveNQUtil(board, col):
#     if col >= N:
#         return True

#     safe_rows = my_filter(lambda row: isSafe(board, row, col), range(N))

#     def tryPlaceQueen(row):
#         # Create a new row where the queen is placed
#         new_row = board[row].set(col, 1)  # Set a queen at the (row, col) position

#         # Create a new board by replacing the updated row
#         new_board = board.set(row, new_row)

#         # Recursively call solveNQUtil with the updated board
#         if solveNQUtil(new_board, col + 1):
#             return True

#         # If no solution, backtrack (remove the queen)
#         new_row = new_row.set(col, 0)  # Backtrack and reset the queen
#         new_board = new_board.set(row, new_row)  # Set the backtracked row back
#         return False

#     return my_reduce(lambda row, acc: acc or tryPlaceQueen(row), safe_rows, False)

# def solveNQ():
#     board = pvector([pvector([0] * N) for _ in range(N)])  # Initialize with immutable pvector

#     if not solveNQUtil(board, 0):
#         print("Solution does not exist")
#         return False

#     printSolution(board)
#     return True

# solveNQ()




##################################################################################################### Working 100%



# # Constants
# N = 8

# def my_reduce(function, list, accumulator):
#     if not list:
#         return accumulator

#     new_accumulator = function(list[0], accumulator)

#     return my_reduce(function, list[1:], new_accumulator)


# def my_map(function, list):
#     return my_reduce(
#         lambda element, accumulator: accumulator + [function(element)], list, []
#     )


# def my_filter(function, list):
#     return my_reduce(
#         lambda element, accumulator: (
#             accumulator + [element] if function(element) else accumulator
#         ),
#         list,
#         [],
#     )


# def my_compose(f, g):
#     return lambda *args: f(g(*args))


# def printSolution(board, i=0, j=0, N=None):

#     if N is None:
#         N = len(board)

#     if i == N:
#         return

#     print(board[i][j], end=" ")

#     if j == N - 1:
#         print()
#         printSolution(board, i + 1, 0, N)
#     else:
#         printSolution(board, i, j + 1, N)

# def check_row_for_conflict_with_map(board, row, col):
#     return any(my_map(lambda i: board[row][i] == 1, range(col)))


# def check_upper_diag_for_conflict_with_map(board, row, col):
#     return any(
#         my_map(
#             lambda i_j: board[i_j[0]][i_j[1]] == 1,
#             list(zip(range(row, -1, -1), range(col, -1, -1))),
#         )
#     )


# def check_lower_diag_for_conflict_with_map(board, row, col):
#     return any(
#         my_map(
#             lambda i_j: board[i_j[0]][i_j[1]] == 1,
#             list(zip(range(row, N), range(col, -1, -1))),
#         )
#     )


# def lambda_test(x):
#     return x


# def check_all_conflicts_composed(board, row, col):
#     return my_compose(
#         lambda x: lambda_test(x)
#         or check_lower_diag_for_conflict_with_map(board, row, col),
#         my_compose(
#             lambda x: x or check_upper_diag_for_conflict_with_map(board, row, col),
#             check_row_for_conflict_with_map,
#         ),
#     )(board, row, col)


# def isSafe(board, row, col):

#     if check_all_conflicts_composed(board, row, col):
#         return False

#     return True


# def solveNQUtil(board, col):
#     if col >= N:
#         return True

#     safe_rows = my_filter(lambda row: isSafe(board, row, col), range(N))

#     def tryPlaceQueen(row):

#         board[row][col] = 1

#         if solveNQUtil(board, col + 1):
#             return True
#         board[row][col] = 0
#         return False

#     return my_reduce(lambda row, acc: acc or tryPlaceQueen(row), safe_rows, False)

# def solveNQ():
#     board = [[0] * N for _ in range(N)]

#     if not solveNQUtil(board, 0):
#         print("Solution does not exist")
#         return False

#     printSolution(board)
#     return True


# solveNQ()
