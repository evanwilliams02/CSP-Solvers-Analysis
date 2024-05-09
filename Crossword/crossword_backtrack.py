global board_intial, iterations


iterations = 0

board_intial = [
    [0,0,0,0,0,0,1,0,1,0,0,0,0,0],
    [0,0,1,0,0,1,1,1,1,1,1,1,0,0],
    [0,0,1,0,0,0,1,1,1,1,1,0,0,0],
    [0,0,1,0,1,1,1,1,0,1,1,1,0,1],
    [0,0,1,1,1,1,1,1,0,1,1,1,1,1],
    [1,1,1,1,1,1,0,1,0,0,1,1,1,1],
    [0,1,1,1,1,1,1,0,0,0,0,0,1,1],
    [0,1,0,1,0,1,0,0,1,1,1,1,1,1],
    [0,1,0,1,0,1,0,0,0,0,1,1,1,1],
    [0,1,0,1,0,0,0,1,0,1,1,1,1,0],
    [0,0,0,1,0,1,1,1,1,1,1,1,1,0],
    [0,0,0,1,0,0,0,1,1,1,1,0,0,0],
    [1,1,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,1,1,1,1,1,1,1,1,1,1]
]

words_placed = []

def read_words_from_file(file_path):
    words = []  

   
    with open(file_path, 'r') as file:
       
        for line in file:
            word = line.strip()  
            words.append(word) 

    return words

def print_board():

    print()

    for i in range(len(board_intial)):
        for j in range(len(board_intial[i])):

            if board_intial[i][j] != 0 and board_intial[i][j] != 1:
                print("\033[1m" + ' ' + board_intial[i][j] +' ', end="" + "\033[0m")
            if board_intial[i][j] == 1:
                print(' x ', end="")
            if board_intial[i][j] == 0:
                print('   ', end="")

        print('\n')
    
    print()

def get_horizontal_seqs(row, row_index):
        sequences = []
        current_sequence = []
        for i, val in enumerate(row):
            if val == 1:
                current_sequence.append((row_index, i))
            elif current_sequence:
                sequences.append(current_sequence)
                current_sequence = []
        if current_sequence:
            sequences.append(current_sequence)
        return sequences

def get_vert_seqs(board):
        coordinates = [[] for _ in range(len(board[0]))]  

        for x, row in enumerate(board):
            for y, val in enumerate(row):
                if val == 1:
                    coordinates[y].append((x, y)) 

        return coordinates

def get_seqs(board):
    global board_intial
    
    
    horizontal_results = []
    for row_index, row in enumerate(board_intial):
        horizontal_results.append(get_horizontal_seqs(row, row_index))

    vertical_results = get_vert_seqs(board_intial)

    return horizontal_results, vertical_results

def filter_verts(two_d_array):
    result = []
    for inner_array in two_d_array:
        temp = []
        for i in range(len(inner_array) - 1):
            temp.append(inner_array[i])
            if inner_array[i+1][0] - inner_array[i][0] > 1:
                result.append(temp)
                temp = []
        temp.append(inner_array[-1])
        result.append(temp)

    return result

def find_coords():
    h, v = get_seqs(board_intial)

    
    filtered_v = filter_verts(v)


    real = []

    for i in h:
        for g in i:
            if len(g) > 1:
                real.append((g, 'h'))

    for i in filtered_v:
            if len(i) > 1:
                real.append((i, 'v'))
    
    return real

def get_cross_coords(h_coords, v_coords):

    coords = []

    crosses = []
    
    for g in h_coords:
        for n in g:
            coords.append(n)
    
    
    for f in v_coords:
        for d in f:
            if d in coords:
                crosses.append(d)
    
    return crosses

def remove_word(board, word, x, y, direction):
    global board_intial

    if direction == 'horizontal':
        for i in range(len(word)):
            board_intial[x][y + i] = 1
    elif direction == 'vertical':
        for i in range(len(word)):
            board_intial[x + i][y] = 1

def check_no_ones():
    for row in board_intial:
        if 1 in row:
            return False 
    return True

def generate_content():
    all_coords = find_coords()

    # crosses = get_cross_coords(h_coords, v_coords)

    crosses = None
    file_path = 'Crossword/words_test.txt'

    word_array = read_words_from_file(file_path)

    return all_coords, crosses, word_array














def is_valid_placement(board, word, x, y, direction, coord_sequence):
    global board_intial, words_placed
    

    if direction == 'horizontal':

        for i, letter in enumerate(word):
            if board_intial[x][y + i] != 1 and board_intial[x][y + i] != letter and len(word) != len(coord_sequence) and word not in words_placed:
                
                return False
        

    elif direction == 'vertical':

        for i, letter in enumerate(word):
            if board_intial[x + i][y] != 1 and board_intial[x + i][y] != letter and len(word) != len(coord_sequence) and word not in words_placed:
                
                return False
        
    return True



def place_word(board, word, x, y, direction):
    global board_intial

    if direction == 'horizontal':

        for i, letter in enumerate(word, start=0):

            print((x,y+i), letter, y, '+', i, direction)
            board_intial[x][y + i] = letter.strip()
            
    elif direction == 'vertical':

        for i, letter in enumerate(word, start=0):

            print((x + i,y), letter, x, '+', i, direction)
            board_intial[x + i][y] = letter.strip()
            
    words_placed.append(word)

    return True


def solve_crossword(board, words, sequences, crosses):
    global board_intial, iterations

    if check_no_ones():
        print('done')
        return True
    
    for word in words:
        if word not in words_placed:
            
            start_x = sequences[iterations][0][0][0]
            start_y = sequences[iterations][0][0][1]

            if sequences[iterations][1] == 'h':
                direction = 'horizontal'
            else:
                direction = 'vertical'
            


            if is_valid_placement(board_intial, word, start_x, start_y, direction, sequences[iterations][0]):
                

                place_word(board_intial, word, start_x, start_y, direction)

                print_board()
                print(sequences[iterations])
                if solve_crossword(board_intial, words, sequences, crosses):
                    iterations += 1
                    return True
                
                print()
                print('removed word')
                print_board()

                words_placed.remove(word)
                remove_word(board_intial, word, start_x, start_y, direction)
                
                
            # if placed:
            #     break
                # remove_word(board_intial, word, x, y, 'horizontal')

                # if solve_crossword(board_intial, words, coord_sequence, crosses):
                #     return True
                
                # remove_word(board_intial, word, x, y, 'vertical')



    return False

    













all_seqs, crosses_initial, word_array_initial = generate_content()


solved = solve_crossword(board_intial, word_array_initial, all_seqs, crosses_initial)
print('solved', solved)