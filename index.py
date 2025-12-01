# ## Battaglia Navale

# Scopo dell'esercizio: Implementare una versione semplificata del gioco da tavolo "Battaglia Navale" utilizzando Python da terminale. Il gioco consisterà in un giocatore contro il computer.  
  
# **Regole del gioco:**  
# - Il campo di gioco sarà una griglia quadrata di dimensioni predefinite (ad esempio 5x5).  
# - Il giocatore e il computer avranno ciascuno una sola nave di dimensione predefinita (ad esempio lunga 3 celle) da posizionare sulla griglia.  
# - Le navi possono essere posizionate orizzontalmente o verticalmente, ma non diagonalmente.  
# - I giocatori si alterneranno nel tentativo di colpire la nave avversaria sparando su una cella della griglia.  
# - Se un colpo colpisce una nave avversaria, verrà segnalato come "colpito" (ad esempio con il simbolo 'X'), altrimenti verrà segnalato come "mancato" (ad esempio con il simbolo 'O').  
# - Il gioco termina quando una delle navi viene completamente colpita.  
# - Verrà visualizzato un messaggio finale che indica il vincitore del gioco. 
 
# **Suggerimenti per l'implementazione:**  
# - Utilizzare una matrice per rappresentare la griglia di gioco.  
# - Nella prima versione, usate posizioni già determinate alla creazione della matrice.  
# - Visualizzare la griglia di gioco dopo ogni colpo effettuato.  
# - Mantenere un conteggio dei colpi effettuati per ciascun giocatore.
# BONUS:
# "Già sparato in questo punto"

import random
import time

# Game settings
GRID_SIZE = 10 # Square matrix 5x5
TOTAL_SHIPS = 3
SHIP_LENGTH = 2
WATER_CHAR = "~"
SHIP_CHAR = "N"
HIT_CHAR = "X"
MISS_CHAR = "O"

# Creates a square matrix
def make_empty_grid(size):
    grid = []

    for i in range(size):
        row = []
        
        for j in range(size):
            row.append(WATER_CHAR)
        
        grid.append(row)

    return grid

# Fancy function to print game's grid
def print_grid(grid, hide_ship=False, Header=None):
    print("-"*10)

    if Header:
        print(Header, end="\n\n")

    print("#", end="")
    for i in range(GRID_SIZE):
        print(f" {i}", end="")
        
    print()
    
    for i in range(GRID_SIZE):
        print(f"{i} ", end="")
        for j in range(GRID_SIZE):
            to_print = grid[i][j]

            if to_print==SHIP_CHAR and hide_ship:
                to_print = WATER_CHAR

            print(to_print, end=" ")
        
        print()

    print("-"*10)

# safely looks at the cords in the grid, if either x or y is out of bounds returns None
def check_cell(grid, x, y):
    true_size = GRID_SIZE-1

    if x > true_size or x < 0 or y > true_size or y < 0:
        return None
    
    return grid[y][x]

# Returns wether there's a ship near that coordinates
def look_for_ships(grid, x, y, check_self=False):
    to_check = [
        [1, 0], # Right
        [-1, 0], # Left
        [0, 1], # Up
        [0, -1] # Down
    ]

    if check_self:
        to_check.append([0, 0])
    
    for i in to_check:
        result = check_cell(grid, x + i[0], y + i[1])

        if result==SHIP_CHAR:
            return True

    return False

def place_ship(grid, ship_length, x, y, horizontal):
    grid_boundary = GRID_SIZE - (ship_length-1) - 1

    if (horizontal and x > grid_boundary) or (not horizontal and y > grid_boundary):
        return "Out of bounds."
    
    # Check for collisions
    for i in range(ship_length):
        if horizontal and look_for_ships(grid, x+i, y, True) or not horizontal and look_for_ships(grid, x, y+i, True):
            return "You can't place ship attached to each other!"
    
    # Place ship
    for i in range(ship_length):
        if horizontal:
            grid[y][x+i] = "N"

        elif not horizontal:
            grid[y+i][x] = "N"

    return "Placed"

def hit_cell(grid, x, y):
    cell_content = check_cell(grid, x, y)

    if cell_content==None or cell_content==MISS_CHAR or cell_content==HIT_CHAR:
        return "You already hit this point!"
    if cell_content!="N":
        grid[y][x] = MISS_CHAR

        return "You didn't find anything there!"

    grid[y][x] = HIT_CHAR

    if look_for_ships(grid, x, y):
        return "Ship was hit, but it didn't sunk yet!"
    else:
        return "Ship was hit and sunk, well played!"

def ask_ship_coords(remaining_ships):
    text = input(f"Insert coords (Ships: {remaining_ships}) (ex: '0 0 h/v'): ")
    coords = text.split(" ")

    # Default alignment is vertical
    if len(coords)==2:
        coords.append("v")

    coords[2] = coords[2]=="h"

    return int(coords[0]), int(coords[1]), bool(coords[2])

def bot_place_ships(grid, ship_count, ship_length):
    grid_boundary = GRID_SIZE - (ship_length-1) - 1
    start_count = ship_count
    total_attempts = 0

    while ship_count > 0:
        total_attempts += 1

        horizontal = random.randint(0, 1) == 0
        x = random.randint(0, grid_boundary)
        y = random.randint(0, grid_boundary)
        result = place_ship(grid, ship_length, x, y, horizontal)

        if result=="Placed":
            ship_count -= 1
            game_event(f"Bot has placed a ship! Remaining ships {ship_count}/{start_count}")

# Used in bot's decisions, so they appear more random
def shuffle_list(list_object):
    for i in range(len(list_object)):
        swap_with = random.randint(0, len(list_object)-1)

        list_object[i], list_object[swap_with] = list_object[swap_with], list_object[i]

# A fancy print function to highlight game events
def game_event(text):
        print(f"[GAME EVENT] {text}")

# Game data
player_grid = make_empty_grid(GRID_SIZE)
bot_grid = make_empty_grid(GRID_SIZE)
# bot_grid = [
#     ["~", "N", "~", "~", "~"],
#     ["~", "N", "~", "N", "~"],
#     ["~", "N", "~", "N", "~"],
#     ["~", "~", "~", "~", "~"],
#     ["~", "~", "N", "N", "~"],
# ]

# These variables are too keep track of sunk ships
player_hit_count = 0
computer_hit_count = 0

# Computer intentions is a list of points (ex [0, 0], [1, 0])
# If it is empty, then it will just generate a random number and hit it
# If bot hits a ship and it didn't sunk, add nearby cells to computer_intentions
# So the bot wil try to sink the ship
computer_intentions = []

game_finished = False
player_turn = True

bot_place_ships(bot_grid, TOTAL_SHIPS, SHIP_LENGTH)

# Placing sequence!
to_place = TOTAL_SHIPS

while to_place>0:
    print_grid(player_grid, False, "Place your ships!")

    x, y, horizontal = ask_ship_coords(to_place)

    result = place_ship(player_grid, SHIP_LENGTH, x, y, horizontal)
    
    if result =="Placed":
        to_place -= 1
        game_event("Your ship was sucessfully placed!")
    else:
        game_event(result)

game_event("Ship placement phase has finished, get ready!")

# TODO: Improve user experience
while not game_finished:
    if player_turn:
        print_grid(bot_grid, True, "It's your turn!")

        coords = input("Insert coords of the point you want to hit (ex: 0 0): ")
        coords = coords.split(" ")

        result = hit_cell(bot_grid, int(coords[0]), int(coords[1]))

        game_event(result)

        if result=="Ship was hit and sunk, well played!":
            player_hit_count += 1

            if player_hit_count >= TOTAL_SHIPS:
                game_event("PLAYER WON, CONGRATULATIONS!")
                game_finished = True

        if result!="You already hit this point!":
            player_turn = False

    else:
        print_grid(player_grid, True, "It's bot's turn!\nEnemy field:")

        intention = None

        if len(computer_intentions)>0:
            intention = computer_intentions.pop()
        else:
            intention = [random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)]

        game_event(f"Bot is hitting {intention}")
        result = hit_cell(player_grid, intention[0], intention[1])

        game_event(f"[Bot] {result}")

        if result=="Ship was hit and sunk, well played!":
            computer_intentions = []
        elif result=="Ship was hit, but it didn't sunk yet!":
            x, y = intention[0], intention[1]

            computer_intentions = [
                [x + 1, y], # Right
                [x - 1, y], # Left
                [x, y + 1], # Up
                [x, y - 1], # Down
            ]

            shuffle_list(computer_intentions)

        if result=="Ship was hit and sunk, well played!":
            computer_hit_count += 1

            if computer_hit_count >= TOTAL_SHIPS:
                game_event("Seems like you lost to a bot, try again!")

                game_finished = True


        if result!="You already hit this point!":
            print_grid(player_grid, False, "Your field:")
            player_turn = True

input()
