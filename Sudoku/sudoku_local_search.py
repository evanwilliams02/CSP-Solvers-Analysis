import random


def print_board(board):

    for i in range(len(board)):

        if i % 3 == 0 and i != 0:
            print("                          ")

        for j in range(len(board[0])):

            if j % 3 == 0 and j != 0:
                print("   ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")


def generate_initial_solution():
    board = [
            [0,0,0,0,0,0,0,0,1],
            [3,1,0,0,0,0,2,0,0],
            [7,0,0,8,0,0,4,0,0],
            [0,0,0,0,0,0,0,0,6],
            [5,0,0,0,0,0,0,0,0],
            [0,0,0,2,8,4,0,0,3],
            [0,6,5,0,0,0,0,3,0],
            [9,2,0,7,0,0,8,0,0],
            [0,0,0,4,1,0,0,0,0]
        ]
    
    for row in range(len(board)):
        for col in range(len(board[0])):

            if board[row][col] == 0:
                board[row][col] = random.randint(1, 9)

    return board

def is_valid_move(board, row, col, num):


    # Check row
    for i in range(len(board[0])):
        if board[row][i] == num and col != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][col] == num and row != i:
            return False

    # Check box
    curr_box_x = col // 3
    curr_box_y = row // 3

    for row_loop in range(curr_box_y * 3, curr_box_y * 3 + 3):
        for col_loop in range(curr_box_x * 3, curr_box_x * 3 + 3):

            if board[row_loop][col_loop] == num and (row_loop,col_loop) != (row,col):
                return False

    return True

def check_duplicates(arr):
    seen = set()
    for num in arr:
        if num in seen:
            return True
        seen.add(num)
    return False

def get_conflicts(board, row, col):
    count = 0

    for k in range(0,9):
        
        # Check row
        for i in range(len(board[0])):
            if check_duplicates(board[i]):
                count += 1

        # Check column
        for i in range(len(board)):
            arr = []
            arr.append(board[i][col])

            if check_duplicates(arr):
                count += 1
            

    # Check box
    curr_box_x = col // 3
    curr_box_y = row // 3

    arr = []

    for row_l  in range(curr_box_y * 3, curr_box_y * 3 + 3):
        for col_l  in range(curr_box_x * 3, curr_box_x * 3 + 3):
            
            arr.append(board[row_l][col_l])
            # print(arr)
            if check_duplicates(arr):
                count += 1
    
    return count
           
def get_best_move(board):
    best_move = None
    min_conflicts = float('inf')
    # print_board(board)

    for row in range(9):
        for col in range(9):
            
            conflicts = get_conflicts(board, row, col)
            print(conflicts)
            if conflicts < min_conflicts:
                min_conflicts = conflicts
                best_move = (row, col)

    return best_move

def local_search_sudoku():
    board = generate_initial_solution()

    while True:
        row, col = get_best_move(board)
        if row is None or col is None:
            break

        best_num = None
        min_conflicts = float('inf')

        for num in range(1, 10):
            if is_valid_move(board, row, col, num):
                board[row][col] = num
                conflicts = get_conflicts(board, row, col)
                if conflicts < min_conflicts:
                    # print(conflicts)
                    # print_board(board)
                    min_conflicts = conflicts
                    best_num = num

        if best_num is not None:
            board[row][col] = best_num

    return board

# Main program
solved_board = local_search_sudoku()
for row in solved_board:
    print(row)
