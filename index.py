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

GRID_SIZE = 5 # Square matrix 5x5
SHIP_LENGTH = 3
WATER_CHAR = "~"
SHIP_CHAR = "N"
HIT_CHAR = "X"
MISS_CHAR = "O"

# Main function which handles game event succession, manages all sub-functions
def play():
    # griglia = make_empty_grid(GRID_SIZE)

    print("Welcome to Battleship - Version 1.0")

def make_empty_grid(size):
    grid = []

    for i in range(size):
        row = []
        
        for j in range(size):
            row.append(WATER_CHAR)
        
        grid.append(row)

    return grid

def print_grid(grid, hide_ship=False):
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

# safely looks at the cords in the grid, if either x or y is out of bounds returns None
def check_cell(grid, x, y):
    true_size = GRID_SIZE-1

    if x > true_size or x < 0 or y > true_size or y < 0:
        return None
    
    return grid[y][x]

# Returns wether there's a ship near that coordinate
# Use this for ship placement and to check if a ship has sunk or not
def look_for_ships(grid, x, y, check_self=False):
    to_check = [
        [1, 0],
        [0, 1],
        [0, -1],
        [-1, 0]
    ]

    if check_self:
        to_check.append([0, 0])
    
    print("DEBUG STARTED")
    for i in to_check:
        result = check_cell(grid, x + i[0], y + i[1])

        print(f"[DEBUG]:", x + i[0], y + i[1], result)
        if result==SHIP_CHAR:
            return True
    
    print("DEBUG FINISHED")

    return False

def place_ship(grid, ship_length, x, y, horizontal):
    boundary = GRID_SIZE - (GRID_SIZE - ship_length-1) # Grid boundary
    print("boundary is", boundary)
    if (horizontal and x > boundary) or (not horizontal and y > boundary):
        return "Out of bounds."
    
    # Check for collisions
    for i in range(ship_length):
        if horizontal and look_for_ships(grid, x+i, y, True):
            return "You can't place ship attached to each other!"
        elif not horizontal and look_for_ships(grid, x, y+i, True):
            return "You can't place ship attached to each other!"
    
   # Check for collisions
    for i in range(ship_length):
        if horizontal:
            grid[y][x+i] = "N"

        elif not horizontal:
            grid[y+i][x] = "N"

    print_grid(grid)

    return "Placed"

def hit_cell(grid, x, y):
    cell_content = check_cell(grid, x, y)

    if cell_content==MISS_CHAR:
        return "You already hit this point!"
    if cell_content!="N":
        grid[y][x] = MISS_CHAR

        return "You didn't find anything there!"

    grid[y][x] = HIT_CHAR

    if look_for_ships(grid, x, y):
        return "Ship was hit, but it didn't sunk yet!"
    else:
        return "Ship was hit and sunk, well played!"

def ask_coords(remaining_ships):
    text = input(f"Insert coords (Ships: {remaining_ships}) (ex: '0 0 true'): ")
    coords = text.split(" ")

    # Default is vertical
    if len(coords)==2:
        coords.append("false")

    coords[2] = coords[2]=="true"

    return int(coords[0]), int(coords[1]), bool(coords[2])

def game_event(text):
        print("-"*10)
        print(text)
        print("-"*10)

# Game data
player_grid = make_empty_grid(GRID_SIZE)
bot_grid = [
    ["~", "N", "~", "~", "~"],
    ["~", "N", "~", "N", "~"],
    ["~", "N", "~", "N", "~"],
    ["~", "~", "~", "~", "~"],
    ["~", "~", "N", "N", "~"],
]

player_hit_count = 0
computer_hit_count = 0
computer_hits = []
game_finished = True
player_turn = True

# Placing sequence!
to_place = 3

print("Your grid:")
while to_place>0:
    print_grid(player_grid)

    x, y, horizontal = ask_coords(to_place)
    print("[DEBUG] Received", x, y, horizontal)
    result = place_ship(player_grid, 2, x, y, horizontal)
    
    if result =="Placed":
        to_place -= 1
        game_event("Your ship was sucessfully placed!")
    else:
        game_event(result)

input()

while not game_finished:
    if player_turn:
        print("It's your turn!")

        # Print grid

        # Ask coords

        # Hit that point
    print("Turn")
