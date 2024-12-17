def my_reduce(function, iter, accumulator):
    if not iter:
        return accumulator

    new_accumulator = function(iter[0], accumulator)

    return my_reduce(function, iter[1:], new_accumulator)


def compose(f, g):
    return lambda *args: f(g(*args))


def find_blank(puz, x="_"):
    """Find the position of a given element in the puzzle (recursively)."""
    if not puz:
        return None
    try:
        j = puz[0].index(x)
        return 0, j
    except ValueError:
        result = find_blank(puz[1:], x)
        if result:
            i, j = result
            return i + 1, j
    return None


def swap_recursive(puzzle, a, b, row=0, col=0, current_row=()):
    """Recursive function to swap two positions in an immutable tuple with bounds check."""
    if row == len(puzzle):
        return ()
    if col == len(puzzle[0]):
        return (current_row,) + swap_recursive(puzzle, a, b, row + 1, 0)

    a_value = (
        puzzle[a[0]][a[1]]
        if 0 <= a[0] < len(puzzle) and 0 <= a[1] < len(puzzle[0])
        else None
    )
    b_value = (
        puzzle[b[0]][b[1]]
        if 0 <= b[0] < len(puzzle) and 0 <= b[1] < len(puzzle[0])
        else None
    )

    current_value = (
        b_value if (row, col) == a else a_value if (row, col) == b else puzzle[row][col]
    )
    return swap_recursive(puzzle, a, b, row, col + 1, current_row + (current_value,))


def state_transition(puz, x1, y1, x2, y2):
    """Move the blank space to a new position if valid using composition."""
    validate_move = lambda: 0 <= x2 < len(puz) and 0 <= y2 < len(puz[0])
    return compose(
        lambda _: swap_recursive(puz, (x1, y1), (x2, y2)),
        lambda _: validate_move() or None,
    )(puz)


def generate_children(puz, level, fval, goal, heuristic):
    """Generate child nodes recursively without mutable state."""
    x, y = find_blank(puz)
    moves = ((x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y))

    def process_moves(moves, acc=()):
        if not moves:
            return acc
        i, j = moves[0]
        new_state = state_transition(puz, x, y, i, j)
        if new_state:
            new_node = {
                "data": new_state,
                "level": level + 1,
                "fval": heuristic(new_state, goal) + level + 1,
            }
            return process_moves(moves[1:], acc + (new_node,))
        return process_moves(moves[1:], acc)

    return process_moves(moves)


def heuristic(start, goal):
    """Functional heuristic: count misplaced tiles recursively."""

    def count_misplaced(s, g, i=0, j=0):
        if i == len(s):
            return 0
        if j == len(s[i]):
            return count_misplaced(s, g, i + 1, 0)
        return int(s[i][j] != g[i][j] and s[i][j] != "_") + count_misplaced(
            s, g, i, j + 1
        )

    return count_misplaced(start, goal)


def solve_puzzle(start, goal, heuristic_func):
    """Main functional loop to solve the puzzle recursively."""

    def process(open_list, closed_list):
        if not open_list:
            return closed_list

        # Sort by fval and pick the current node
        open_list = tuple(sorted(open_list, key=lambda x: x["fval"]))
        current = open_list[0]
        closed_list += (current,)

        # Goal Check
        if heuristic_func(current["data"], goal) == 0:
            return closed_list

        # Generate children
        children = generate_children(
            current["data"], current["level"], current["fval"], goal, heuristic_func
        )
        new_open_list = open_list[1:] + children

        return process(new_open_list, closed_list)

    start_node = {"data": start, "level": 0, "fval": heuristic_func(start, goal)}
    return process((start_node,), ())


def print_solution(solution):
    """Print the sequence of steps from start to goal recursively."""

    def print_step(steps):
        if not steps:
            return
        step = steps[0]
        print(f"Level: {step['level']}")

        def print_row(data, idx=0):
            if idx == len(data):
                return
            print(data[idx])
            print_row(data, idx + 1)

        print_row(step["data"])
        print()
        print_step(steps[1:])

    print_step(solution)


# Input and Execution
if __name__ == "__main__":

    def get_user_input():
        print("Enter the 3x3 puzzle row by row, use '_' for the blank space:")

        def input_row(n=3, rows=()):
            if n == 0:
                return rows
            row = tuple(input(f"Row {len(rows) + 1}: ").split())
            return input_row(n - 1, rows + (row,))

        return input_row()

    print("Enter the start state:")
    start_state = get_user_input()
    print("Enter the goal state:")
    goal_state = get_user_input()

    # Solve the puzzle using composition
    composed_solver = compose(
        print_solution, lambda s: solve_puzzle(s, goal_state, heuristic)
    )
    print("\nSteps to solve the puzzle:")
    composed_solver(start_state)
