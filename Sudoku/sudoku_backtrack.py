import time

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

def backtrack(board):

    solved = find_empty_cell(board)

    if not solved:
        return True
    else:
        row, col = solved

    for num in range(1,10):

        if valid_board(board, num, (row, col)):
            board[row][col] = num

            if backtrack(board):
                return True

            board[row][col] = 0

    return False

def find_empty_cell(board):

    for row in range(len(board)):
        for col in range(len(board[0])):

            if board[row][col] == 0:
                return (row, col)  # row, col

    return None

def valid_board(board, num, pos):

    # Check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    curr_box_x = pos[1] // 3
    curr_box_y = pos[0] // 3

    for row in range(curr_box_y * 3, curr_box_y * 3 + 3):
        for col in range(curr_box_x * 3, curr_box_x * 3 + 3):

            if board[row][col] == num and (row,col) != pos:
                return False

    return True

print()
print_board(board)

start_time = time.time()

backtrack(board)
print()
print('------------------------')
print()
print_board(board)
print()

end_time = time.time()

print('Board Solved !')
print()
elapsed_time = end_time - start_time

print("Elapsed time: {:.2f} seconds".format(elapsed_time))
print()