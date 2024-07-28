
import numpy as np
import pandas as pd


MAX_GAME_SIZE = 30
N_ROWS = 0
N_COLS = 0
N_MINES = 0
MINE_TOKEN = 'X'
HIDDEN_CELL_TOKEN = u"\u2588"


### GAME SET-UP ###

def mines_coordinates_picker() -> list[tuple]:
    """ Return randomly picked coordinates on grid for specified number of mines """
    mines_y_x_coordinates = []
    while len(mines_y_x_coordinates) < N_MINES:
        random_y_x_coordinates = (int(np.random.randint(N_ROWS, size=1)),
                                  int(np.random.randint(N_COLS, size=1)))
        if random_y_x_coordinates not in mines_y_x_coordinates:
            mines_y_x_coordinates.append(random_y_x_coordinates)
    return mines_y_x_coordinates

def adjacent_cells(y: int, x: int) -> list[tuple]:
    """ Return coordinates of all adjacent cells to a given coordinate """
    adj_cells = []
    adj_cells.append((y+1, x-1))
    adj_cells.append((y+1, x))
    adj_cells.append((y+1, x+1))
    adj_cells.append((y, x-1))
    adj_cells.append((y, x+1))
    adj_cells.append((y-1, x-1))
    adj_cells.append((y-1, x))
    adj_cells.append((y-1, x+1))
    # filter for values that are in correct range
    adj_cells_out = [(y, x) for y, x in adj_cells if all([y>=0, x>=0, y<N_ROWS, x<N_COLS])]
    return adj_cells_out

def set_up_game() -> tuple[list]:
    """ Create all necessary elements for running the game """
    # Pick mine coordinates
    mines_y_x_coordinates = mines_coordinates_picker()
    # Create 0-grid and populate with mines (MINE_TOKEN) 
    grid = [[0]*N_COLS for _ in range(N_ROWS)]
    for y, x in mines_y_x_coordinates:
        grid[y][x] = MINE_TOKEN
    # Compute number of mines in adjacent cells
    for row, col in mines_y_x_coordinates:
        adj_cells = adjacent_cells(y=row, x=col)
        for adj_row, adj_col in adj_cells:
            if grid[adj_row][adj_col] != MINE_TOKEN:
                grid[adj_row][adj_col] += 1
    # Create player-visible grid
    visible_grid = [[HIDDEN_CELL_TOKEN]*N_COLS for _ in range(N_ROWS)]
    # create empty set for coordinates of already revealed cells
    revealed_fields_coordinates = set()
    return grid, visible_grid, mines_y_x_coordinates, revealed_fields_coordinates


### GAME MECHANICS ###

def reveal_empty_fields(y: int, x: int, grid: list, visible_grid: list, revealed_fields_coordinates: set) -> tuple[list]:
    """ Add cells adjacent to selection to revealed_field_coordinates if selected cell is empty """
    def reveal(y: int, x: int) -> None:
        """ Recursively search through and store adjacent empty cells to be revealed """
        if ((y>=0 and y<N_COLS) and (x>=0 and x<N_ROWS) and (y, x) not in revealed_fields_coordinates):
            if grid[y][x] == 0:
                revealed_fields_coordinates.add((y, x))
                adj_cells = adjacent_cells(y, x)
                for y, x in adj_cells:
                    reveal(y, x)
            if grid[y][x] > 0:
                revealed_fields_coordinates.add((y, x))
    reveal(y, x)
    # Set coordinates of revealed tiles to value of game grid.
    for y, x in revealed_fields_coordinates:
        visible_grid[y][x] = grid[y][x]
    return visible_grid, revealed_fields_coordinates


def turn(y: int, x: int, visible_grid: list, revealed_fields_coordinates: set) -> bool:
    """ Determine action and status of game """
    # If selected cell contains mine, end game and reveal position of all mines
    if grid[y][x] == MINE_TOKEN:
        print('\nGAME OVER :(\n')
        for y, x in mines_y_x_coordinates:
            visible_grid[y][x] = MINE_TOKEN
        print(pd.DataFrame(visible_grid).replace(0,''))
        return False
    # If selected cell is empty, call reveal function
    if grid[y][x] == 0:
        visible_grid, revealed_fields_coordinates = reveal_empty_fields(y, x, grid, visible_grid, revealed_fields_coordinates)
    # If selected cell contains non-zero value (i.e. mine count), reveal cell and add coordinates to revealed set.
    if grid[y][x] > 0:
        visible_grid[y][x] = grid[y][x]
        revealed_fields_coordinates.add((y,x))
    # Check if game is won, i.e. the number of revealed cells equals the number of non-mine cells.
    if len(revealed_fields_coordinates) == N_COLS*N_ROWS - len(mines_y_x_coordinates):
        print('\nYOU WON! CONGRATULATIONS :)\n')
        print(pd.DataFrame(visible_grid).replace(0,''))
        return False
    print(pd.DataFrame(visible_grid).replace(0,''))
    return True


### USER INPUT CHECKS ###

def check_user_input_size(user_input: str) -> bool:
    if len(user_input.split()) != 2:
        print('Invalid input, please provide exactly two numbers, for example "10 10"')
        return False
    if not all(input_value.isdigit() for input_value in user_input.split()):
        print('Invalid input, please provide only positive integer, for example "10 10"')
        return False
    if any(input_value <= 0 for input_value in map(int, user_input.split())):
        print(f'Invalid input, selected values must be greater than 0')
        return False
    if any(input_value > MAX_GAME_SIZE for input_value in map(int, user_input.split())):
        print(f'Size too large, please select values smaller than {MAX_GAME_SIZE}')
        return False
    return True

def check_user_input_n_mines(user_input: str) -> bool:
    if len(user_input.split()) != 1:
        print('Invalid input, please provide exactly one number, for example "10"')
        return False
    if not user_input.isdigit():
        print('Invalid input, please provide only positive integer numbers, for example "10 10"')
        return False
    if int(user_input) <= 0:
        print(f'Invalid input, selected value must be greater than 0')
        return False
    if int(user_input) > N_COLS*N_ROWS:
        print(f'Number of mines exceeds number of cells, please select values smaller than {N_COLS*N_ROWS}')
        return False
    return True

def check_user_input_coordinates(user_input: str) -> bool:
    if len(user_input.split()) != 2:
        print('Invalid input, please provide exactly two numbers, for example "10 10"')
        return False
    if not all(input_value.isdigit() for input_value in user_input.split()):
        print('Invalid input, please provide only positive integer, for example "10 10"')
        return False
    y, x = map(int, user_input.split()) 
    if any([y<0, x<0, y>=N_COLS, x>=N_ROWS]):
        print(f'Invalid input! Please enter values between 0-{N_COLS} for y and 0-{N_ROWS} for x')
        return False
    return True


### USER INPUTS ###

def get_user_input_size() -> tuple[int]:
    is_input_valid = False
    while not is_input_valid:
        user_input = input('Please enter the desired size of the minefield (number of columns, rows): ')
        is_input_valid = check_user_input_size(user_input)
    return map(int, user_input.split())

def get_user_input_n_mines() -> int:
    is_input_valid = False
    while not is_input_valid:
        user_input = input('Please enter the number of mines on the minefield: ')
        is_input_valid = check_user_input_n_mines(user_input)
    return int(user_input)

def get_user_input_coordinates() -> tuple[int]:
    is_input_valid = False
    while not is_input_valid:
        user_input = input('\nEnter coordinates y and x. Press CTRL+C to end the game. ')
        is_input_valid = check_user_input_coordinates(user_input)
    return map(int, user_input.split()) 


### RUN GAME ###

def main():
    # Define global objects
    global grid, mines_y_x_coordinates, N_COLS, N_ROWS, N_MINES
    # Get initial user preferences (game parameters)
    N_COLS, N_ROWS = get_user_input_size()
    N_MINES = get_user_input_n_mines()
    # Set up game and display grid
    grid, visible_grid, mines_y_x_coordinates, revealed_fields_coordinates = set_up_game()
    print(pd.DataFrame(visible_grid))
    # Run game
    game_running = True
    while game_running:
        y, x = get_user_input_coordinates()
        game_running = turn(y, x, visible_grid, revealed_fields_coordinates)



if __name__ == '__main__':
    main()