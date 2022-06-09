def get_empty_board():
    board = ["_", "_", "_",
             "_", "_", "_",
             "_", "_", "_"]
    return board

board = get_empty_board()
game_still_on = True
current_player = "X"
winner = None

def display_board():

    print(board[0] + " | " + board[1] + " | " + board[2])
    print(board[3] + " | " + board[4] + " | " + board[5])
    print(board[6] + " | " + board[7] + " | " + board[8])

def check_if_game_end():
    check_if_win()
    check_if_tie()

def check_if_win():
    global winner
    row_winner = check_rows()
    column_winner = check_columns()
    diagonal_winner = check_diagonals()

    if row_winner:
        winner = row_winner
    elif column_winner:
        winner = column_winner
    elif diagonal_winner:
        winner = diagonal_winner
    else:
        winner = None
    return

def check_rows():
    global game_still_on
    row_1 = board[0] == board[1] == board[2] != "_"
    row_2 = board[3] == board[4] == board[5] != "_"
    row_3 = board[6] == board[7] == board[8] != "_"

    if row_1 or row_2 or row_3:
        game_still_on = False
    if row_1:
        return board[0]
    elif row_2:
        return board[3]
    elif row_3:
        return board[6]
    return

def check_columns():
    global game_still_on
    column_1 = board[0] == board[3] == board[6] != "_"
    column_2 = board[1] == board[4] == board[7] != "_"
    column_3 = board[2] == board[5] == board[8] != "_"

    if column_1 or column_2 or column_3:
        game_still_on = False
    if column_1:
        return board[0]
    elif column_2:
        return board[1]
    elif column_3:
        return board[2]
    return

def check_diagonals():
    global game_still_on
    diagonal_1 = board[0] == board[4] == board[8] != "_"
    diagonal_2 = board[6] == board[4] == board[2] != "_"

    if diagonal_1 or diagonal_2:
        game_still_on = False
    if diagonal_1:
        return board[0]
    elif diagonal_2:
        return board[6]
    return

def check_if_tie():
    global  game_still_on
    if "_" not in board:
        game_still_on = False
    return

def flip_player():
    global current_player
    if current_player == "X":
        current_player = "O"
    elif current_player == "O":
        current_player = "X"
    return

def handle_turn(player):

    valid_position = False
    print(player + " 's turn.")
    position = input("Please choose a position from 1 to 9: ")

    while not valid_position:
        while position not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            position = input("Wrong Input! Please choose a position from 1 to 9: ")

        position = int(position) - 1

        if board[position] == "_":
            valid_position = True
        else:
            print("Position taken! ")

    board[position] = player
    display_board()

def play_game():
    display_board()

    while game_still_on:
        handle_turn(current_player)

        check_if_game_end()

        flip_player()
    if winner == "X" or winner == "O":
        print(f"The winner is {winner} player!")
    elif winner == None:
        print("The game ends in tie!")

def main_menu():
    play_game()

if __name__ == "__main__":
    main_menu()