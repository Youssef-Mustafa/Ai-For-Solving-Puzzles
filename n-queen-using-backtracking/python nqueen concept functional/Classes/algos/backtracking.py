from time import sleep, time


# from pyrsistent import pvector

# Using PVector ---------------------------------------------------------------------------------------------------

# N = 0

# def my_reduce(function, iter, accumulator):
#     if not iter:
#         return accumulator

#     new_accumulator = function(iter[0], accumulator)

#     return my_reduce(function, iter[1:], new_accumulator)


# def my_map(function, iter):
#     return my_reduce(
#         lambda element, accumulator: accumulator + (function(element),), iter, pvector(())
#     )


# def my_filter(function, iter):
#     return my_reduce(
#         lambda element, accumulator: (
#             accumulator + (element,) if function(element) else accumulator
#         ),
#         iter,
#         pvector(()),
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
#             pvector(zip(range(row, -1, -1), range(col, -1, -1))),
#         )
#     )


# def check_lower_diag_for_conflict_with_map(board, row, col):
#     return any(
#         my_map(
#             lambda i_j: board[i_j[0]][i_j[1]] == 1,
#             pvector(zip(range(row, N), range(col, -1, -1))),
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

# def update_board(board, row, col, value):
#     new_row = board[row].set(col, value)

#     new_board = board.set(row, new_row)

#     return new_board


# def solveNQUtil(board, col, add_q, remove_q, append_q, pop_q):
#     if col >= N:
#         return board

#     safe_rows = my_filter(lambda row: isSafe(board, row, col), range(N))

#     sleep(0.1)

#     def tryPlaceQueen(row):

#         add_q(row, col)
#         new_board = update_board(board, row, col, 1)
#         pop_q()

#         printSolution(board)
#         print()

#         result = solveNQUtil(
#             new_board,
#             col + 1,
#             add_q=add_q,
#             remove_q=remove_q,
#             append_q=append_q,
#             pop_q=pop_q,
#         )

#         if result:
#             printSolution(result)
#             print()
#             return result

#         new_board = update_board(board, row, col, 0)
#         remove_q(row, col)
#         append_q()

#         return False

#     return my_reduce(lambda row, acc: acc or tryPlaceQueen(row), safe_rows, False)

# def solveNQ(event, board_cell, add_q, remove_q, append_q, pop_q):

#     global N
#     N = board_cell

#     board = pvector(pvector([0] * board_cell) for _ in range(N))

#     start_time = time()
#     solved_board = solveNQUtil(
#         board=board,
#         col=0,
#         add_q=add_q,
#         remove_q=remove_q,
#         append_q=append_q,
#         pop_q=pop_q,
#     )

#     if not solved_board:
#         print("Solution does not exist")
#         return False
#     printSolution(solved_board)
#     print()
#     end_time = time()
#     event.set()
#     print("elapsed_time => ", end_time - start_time)
#     return solved_board

# Using Tuples -------------------------------------------------------------------------------------------

N = 0


def my_reduce(function, iter, accumulator):
    if not iter:
        return accumulator

    new_accumulator = function(iter[0], accumulator)

    return my_reduce(function, iter[1:], new_accumulator)


def my_map(function, iter):
    return my_reduce(
        lambda element, accumulator: accumulator + (function(element),), iter, tuple(())
    )


def my_filter(function, iter):
    return my_reduce(
        lambda element, accumulator: (
            accumulator + (element,) if function(element) else accumulator
        ),
        iter,
        tuple(()),
    )


def my_compose(f, g):
    return lambda *args: f(g(*args))


def set_tuple(mutable, index, value):
    return tuple(mutable[:index] + (value,) + mutable[index + 1 :])


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
            tuple(zip(range(row, -1, -1), range(col, -1, -1))),
        )
    )


def check_lower_diag_for_conflict_with_map(board, row, col):
    return any(
        my_map(
            lambda i_j: board[i_j[0]][i_j[1]] == 1,
            tuple(zip(range(row, N), range(col, -1, -1))),
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


def update_board(board, row, col, value):
    new_row = set_tuple(board[row], col, value)

    new_board = set_tuple(board, row, new_row)

    return new_board


def solveNQInTerm(board, col):
    if col >= N:
        return board

    safe_rows = my_filter(lambda row: isSafe(board, row, col), range(N))

    sleep(0.1)

    def tryPlaceQueen(row):

        new_board = update_board(board, row, col, 1)

        printSolution(board)
        print()

        result = solveNQInTerm(
            new_board,
            col + 1,
        )

        if result:
            printSolution(result)
            print()
            return result

        new_board = update_board(board, row, col, 0)

        return False

    return my_reduce(lambda row, acc: acc or tryPlaceQueen(row), safe_rows, False)


def solve_in_termenal():

    global N

    board = (
        (0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0),
    )

    N = len(board)

    start_time = time()
    solved_board = solveNQInTerm(
        board=board,
        col=0,
    )

    if not solved_board:
        print("Solution does not exist")
        return False
    printSolution(solved_board)
    print()
    end_time = time()
    print("elapsed_time => ", end_time - start_time)
    return solved_board


print(solve_in_termenal())


def solveNQUtil(board, col, add_q, remove_q, append_q, pop_q):
    if col >= N:
        return board

    safe_rows = my_filter(lambda row: isSafe(board, row, col), range(N))

    sleep(0.1)

    def tryPlaceQueen(row):

        add_q(row, col)
        new_board = update_board(board, row, col, 1)
        pop_q()

        printSolution(board)
        print()

        result = solveNQUtil(
            new_board,
            col + 1,
            add_q=add_q,
            remove_q=remove_q,
            append_q=append_q,
            pop_q=pop_q,
        )

        if result:
            printSolution(result)
            print()
            return result

        new_board = update_board(board, row, col, 0)
        remove_q(row, col)
        append_q()

        return False

    return my_reduce(lambda row, acc: acc or tryPlaceQueen(row), safe_rows, False)


def solveNQ(event, board_cell, add_q, remove_q, append_q, pop_q):

    global N
    N = board_cell

    board = tuple(tuple([0] * board_cell) for _ in range(N))

    start_time = time()
    solved_board = solveNQUtil(
        board=board,
        col=0,
        add_q=add_q,
        remove_q=remove_q,
        append_q=append_q,
        pop_q=pop_q,
    )

    if not solved_board:
        print("Solution does not exist")
        return False
    printSolution(solved_board)
    print()
    end_time = time()
    event.set()
    print("elapsed_time => ", end_time - start_time)
    return solved_board
