import random
import os
import time
import pandas as pd


# INTRODUCTION/WELCOME SCREEN
# For Clearing Console on Start...
# 'clear' - For Unix(Bash) | 'cls' - For Windows(CMD)

os.system('clear')
print("Welcome to 2048")
print("--------")
print("CONTROLS")
print("--------")
print("u - Slide Up")
print("d - Slide Down")
print("l - Slide Left")
print("r - Slide Right")
print("-------------------------")
user_name = input("ENTER USERNAME TO PROCEED: ")
os.system('clear')

# Asking user the size of the Grid
size = int(input("Choose the size of the Grid (Minimum: 4, Maximum: 10): "))
while size < 4 or size > 10:
    print("\nGrid size is Out of bounds...")
    size = int(input("Enter Grid Size Again: "))

# Max Size of a tile, obtaining which results in VICTORY (Default - 2048)
max_tile = 2048

# List from which a number can be chosen to be inserted at an empty tile
insert_tiles = [2, 4]

# Original Matrix/Grid
m = [[0 for i in range(size)] for j in range(size)]

# Global declaration of time variables
mins = 0
sec = 0

# Count of Moves
move_count = int(0)

# Permitted/Allowed moves : Used while taking inp_move from user
allowed_moves = ['L', 'l', 'U', 'u', 'R', 'r', 'D', 'd']

# Special Case - Used when possibility of moves when all tiles are filled is to be checked
x_lock = False
y_lock = False


# ==================== FUNCTIONS ==================== #

# pr_cyan() : To print Cyan-colored output
def pr_cyan(in_str): print("\033[96m {}\033[00m" .format(in_str)) 

# get_random_X() : Choosing Random Row Number for placing either of 2 or 4
def get_random_X():
    x = random.randrange(0, size)
    return x


# get_random_Y() : Choosing Random Column Number for placing either of 2 or 4
def get_random_Y():
    y = random.randrange(0, size)
    return y


# transpose() : To perform transpose operation on the Matrix
def transpose():
    temp = [[0 for i in range(size)] for j in range(size)]
    for i in range(0, size):
        for j in range(0, size):
            temp[j][i] = m[i][j]
    for i in range(0, size):
        for j in range(0, size):
            m[i][j] = temp[i][j]


# left_shift(i) : Shifting all non-zero numbers in Row "i" towards left
def left_shift(i):
    l_ptr = 0
    non_zero_list = []

    # Appending non-zero elements of Row "i" to non_zero_list
    for j in range(0, size):
        if (m[i][j] != 0):
            non_zero_list.append(m[i][j])
            m[i][j] = 0

    for j in non_zero_list:
        m[i][l_ptr] = j
        l_ptr += 1


# right_shift(i) : Shifting all non-zero numbers in Row "i" towards right
def right_shift(i):
    r_ptr = size - 1
    non_zero_list = []

    # Appending non-zero elements of Row "i" to non_zero_list
    for j in range(size - 1, -1, -1):
        if (m[i][j] != 0):
            non_zero_list.append(m[i][j])
            m[i][j] = 0

    for j in non_zero_list:
        m[i][r_ptr] = j
        r_ptr -= 1


# end_game() : Checking for the Endgame Condition (checking for two conditions: 2048 <OR> No Empty Tiles)
def end_game():
    # | Values of "game_status" | 0 - BEING CONTINUED | 1 - VICTORY | 2 - DEFEAT | #
    # | Values of "empty_tiles" | 0 - NO TILE IS EMPTY | 1 - EMPTY TILES EXIST | #
    game_status = 0
    empty_tiles = 0

    # Checking if the max tile is obtained (if yes, VICTORY)
    for i in range(0, size):
        for j in range(0, size):
            if (m[i][j] == max_tile):
                game_status = 1
                break
        if game_status == 1:
            break

    # Checking if any of the tiles are empty (if not, DEFEAT)
    for i in range(0, size):
        for j in range(0, size):
            if (m[i][j] == 0):
                empty_tiles = 1
                break
        if empty_tiles == 1:
            break

    if empty_tiles == 0 and neighbor_chk():
        game_status = 2

    return game_status

# neighbor_chk() : Called when no tile is empty. Checks if there are any valid moves possible. If no moves possible, then returns True so that game_status is set to 2. Else, Modifies allowed_moves accordingly
def neighbor_chk():
    global x_lock
    global y_lock
    global allowed_moves

    x_lock = True
    y_lock = True
    allowed_moves = []
    for i in range(0, size):
        for j in range(0, size - 1):
            if m[i][j] == m[i][j + 1]:
                x_lock = False
                allowed_moves.extend(['l', 'L', 'r', 'R'])
                break
    transpose()
    for i in range(0, size):
        for j in range(size - 1, 0, -1):
            if m[i][j] != 0 and m[i][j] == m[i][j - 1]:
                y_lock = False
                allowed_moves.extend(['u', 'U', 'd', 'D'])
                break
    transpose()
    return x_lock and y_lock

# display_grid() : function to print the matrix
def display_grid():
    # For Clearing Console every iteration...
    # 'clear' - For Unix(Bash) | 'cls' - For Windows(CMD)
    global mins
    global sec
    os.system('clear')
    end = time.time()
    t = int(end - start)
    mins = int(t/60)
    sec = t % 60
    print("Time elapsed:", mins, "minute(s) :", sec, "second(s)")
    print("Moves:", move_count, "\n")
    for i in range(len(m)):
        for j in range(len(m[i])):
            print("| {:4d}".format(m[i][j]),
                  end=" ") if m[i][j] != 0 else print("|", end="      ")
        print("|")
    if x_lock:
        print("\n(!) SLIDING HORIZONTALLY IS INVALID")
    if y_lock:
        print("\n(!) SLIDING VERTICALLY IS INVALID")


# gen_random_tile() : Function to generate a random place in matrix, if it is 0 put a random integer 2 or 4 in that place
def gen_random_tile():
    while True:
        rx = get_random_X()
        ry = get_random_Y()
        if(m[rx][ry] == 0):
            break

    m[rx][ry] = random.choice(insert_tiles)


# main_logic() : Reading user move and performing the respective operation
def main_logic():
    global move_count
    global allowed_moves
    global x_lock
    global y_lock

    inp_move = input("\nEnter Your Move: ")
    move_count += 1
    while inp_move not in allowed_moves:
        print("INVALID INPUT")
        inp_move = input("Enter your Move again: ")

    # If the move is either LEFT or UP
    if inp_move in ['L', 'l', 'U', 'u']:
        if inp_move in ['u', 'U']:
            transpose()
        for i in range(0, size):
            left_shift(i)
            for j in range(0, size - 1):
                if m[i][j] == m[i][j + 1]:
                    m[i][j] = 2 * m[i][j]
                    m[i][j + 1] = 0
                    # break
            left_shift(i)
        if inp_move in ['u', 'U']:
            transpose()

    # ELSE IF the move is either RIGHT or DOWN
    elif inp_move in ['R', 'r', 'D', 'd']:
        if inp_move in ['d', 'D']:
            transpose()
        for i in range(0, size):
            right_shift(i)
            for j in range(size - 1, 0, -1):
                if m[i][j] != 0 and m[i][j] == m[i][j - 1]:
                    m[i][j] = 2 * m[i][j]
                    m[i][j - 1] = 0
                    # break
            right_shift(i)
        if inp_move in ['d', 'D']:
            transpose()
    
    # RESETTING ALLOWED INPUTS & LOCKS - This is because the following
    # values are altered if the previous move had all tiles filled but 
    # matching neighbors existed
    allowed_moves = ['L', 'l', 'U', 'u', 'R', 'r', 'D', 'd']
    x_lock = False
    y_lock = False


def find_max_tile():
    max_in_each_row = [max(row) for row in m]
    return max(max_in_each_row)

# display_leaderboard() : To display the leaderboard
def display_leaderboard(status):
    leaderboard_df = pd.read_csv('leaderboard.csv', index_col=False)
    max_tile_scored = find_max_tile()
    
    new_user = {
        "Username": user_name,
        "Moves": move_count,
        "Time": str(mins) + " minute(s) " + str(sec) + " second(s)",
        "MaxTile": max_tile_scored
    }

    leaderboard_df.loc[len(leaderboard_df.index)] = new_user
    leaderboard_df = leaderboard_df.sort_values(by=['MaxTile', 'Moves'], ascending=[False, True])
    leaderboard_df.reset_index(drop=True, inplace=True)
    
    print("\n-----------")
    print("LEADERBOARD")
    print("-----------")
    print(leaderboard_df.head(10))

    print("\n----------")
    print("YOUR STATS")
    print("----------")
    for key, val in new_user.items():
        print("{} : {}".format(key, val))

    leaderboard_df.to_csv('leaderboard.csv', index=False)
    



# ==================== MAIN CODE ==================== #

# GAME MECHANICS
# Calling gen_random_tile() function twice to generate either of the tiles 2, 4 at random, empty(0-Tile) places
gen_random_tile()
gen_random_tile()
start = time.time()

# Loop which runs until the Max tile (2048-Tile) is obtained OR no empty tile (0-Tile) remains
while (end_game() == 0):
    display_grid()
    main_logic()
    status = end_game()
    if status == 0:
        gen_random_tile()

display_grid()

if status == 1:
    print("------------- ")
    pr_cyan("YOU WIN 😎")
    print("-------------")
    display_leaderboard(status)
else:
    print(" ------------ ")
    pr_cyan("YOU LOSE 😫")
    print(" ------------ ")
    display_leaderboard(status)
