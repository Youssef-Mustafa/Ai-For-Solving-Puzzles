from time import sleep, time


class BackTracking():
    def __init__(self, n_queens, ncanvas, col) -> None:
        self.n_queens = n_queens
        self.ncanvas = ncanvas
        self.board = ncanvas.board
        self.col = col
        self.algorithm = 'BackTracking'
        self.found_sol = False

    def is_safe(self, board, row, col):
        
        row_safe = self.row_check(board, row)
        col_safe = self.col_check(board, row, col)
        diagonal_safe = self.diagonal_check(board, row, col)
        return row_safe and col_safe and diagonal_safe

    def row_check(self, board, row):
        return not board[row].__contains__(1)

    def col_check(self, board, row, col):
        for c in range(col):
            if board[row][c] == 1:
                return False
        return True

    def diagonal_check(self, board, row, col):
        upper_right = True
        upper_left = True
        lower_right = True
        lower_left = True

        temp_row = row + 1
        temp_col = col + 1

        # check lower_right
        while temp_row < self.n_queens and temp_col < self.n_queens:
            if board[temp_row][temp_col] == 1:
                lower_right = False
                break
            temp_row += 1
            temp_col += 1

        # check lower_left
        temp_row = row + 1
        temp_col = col - 1
        while temp_row < self.n_queens and temp_col >= 0:
            if board[temp_row][temp_col] == 1:
                lower_left = False
                break
            temp_col -= 1
            temp_row += 1

        # check upper_right
        temp_row = row - 1
        temp_col = col + 1
        while temp_row >= 0 and temp_col < self.n_queens:
            if board[temp_row][temp_col] == 1:
                upper_right = False
                break
            temp_col += 1
            temp_row -= 1

        # check upper_left
        temp_row = row - 1
        temp_col = col - 1
        while temp_row >= 0 and temp_col >= 0:
            if board[temp_row][temp_col] == 1:
                upper_left = False
                break
            temp_col -= 1
            temp_row -= 1

        return upper_left and upper_right and lower_left and lower_right


    
    def backtrack_algo(self, col):
                            
        if col >= self.n_queens:
            return True
                      
           
        for row in range(self.n_queens):
            
            is_safe = self.is_safe(self.board, row, col)
                        
            self.ncanvas.add_queen(row,col)

            sleep(0.01)
            
            if is_safe:
                self.board[row][col] = 1
                self.ncanvas.pop_queens()
                
                if self.backtrack_algo(col + 1):                  
                    return True
                
                self.board[row][col] = 0 
                self.ncanvas.remove_queen(row,col)
                self.ncanvas.append_queens()
                
            else:
                self.board[row][col] = 0 
                self.ncanvas.remove_queen(row,col)
                
                
        return False
    
    
    def run(self, event):
        start_time = time()
        while True:
            self.backtrack_algo(0)
            
            if self.row_check(self.board, 1):
                self.board[0][self.col] = 0
                self.col = (self.col + 1) % self.n_queens
                self.board[0][self.col] = 1
                self.ncanvas.reset_board()
            else:
                print("he5o he5o")
                print(self.board)
                self.found_sol = True
                end_time = time()
                event.set()
                print("elapsed_time => ", end_time - start_time)
                break
