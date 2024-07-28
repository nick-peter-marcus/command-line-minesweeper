# command-line-minesweeper
This repository contains the python script of a small minesweeper game which can be launched and run in the terminal. The code implements the basic game play and logic.

Some screenshots:

![01_launch_game](https://github.com/nick-peter-marcus/command-line-minesweeper/images/01_launch_game.png?raw=true)

![02_pick_and_reveal_coordinates](https://github.com/nick-peter-marcus/command-line-minesweeper/images/02_pick_and_reveal_coordinates.png?raw=true)

![03_game_won](https://github.com/nick-peter-marcus/command-line-minesweeper/images/03_game_won.png?raw=true)

![04_game_over](https://github.com/nick-peter-marcus/command-line-minesweeper/images/04_game_over.png?raw=true)


Some improvements to be made:
- Efficiency: Under current configuration, maximum recursion levels are reached when number of cells (defined by specified number of rows and columns) exceeds 1000.
- Code:
    - Input check functions can potentially be consolidated
    - Make use of classes instead of lists
- Gameplay:
    - Have a proper way of exiting the game
    - Set up game after first coordinates were provided in order to prevent losing in first move.
    - Display number of rounds and time
    - Allow input of multiple cells to be revealed
- Pygame:
    - Create interactive game app
