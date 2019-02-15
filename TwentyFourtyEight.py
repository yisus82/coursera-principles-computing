"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    result = [0 for dummy_var in range(len(line))]
    index = 0
    for tile in line:
        if tile != 0:
            if result[index] == 0:
                result[index] = tile
            elif result[index] == tile:
                result[index] += tile
                index += 1
            else:
                index += 1
                result[index] = tile
    return result


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        up_list = [(0, col) for col in range(grid_width)]
        down_list = [(grid_height - 1, col) for col in range(grid_width)]
        left_list = [(row, 0) for row in range(grid_height)]
        right_list = [(row, grid_width - 1) for row in range(grid_height)]
        self.initial_tiles = {UP: up_list, DOWN: down_list, LEFT: left_list, RIGHT: right_list}
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self.grid = [[0 for dummy_col in range(self.grid_width)] for dummy_row in range(self.grid_height)]

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        grid_str = ""
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                grid_str += str(self.grid[row][col])
            grid_str += "\n"
        return grid_str

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        offset = OFFSETS[direction]
        changed = False
        if direction == UP or direction == DOWN:
            num_iter = self.grid_height
        else:
            num_iter = self.grid_width
        for tile in self.initial_tiles[direction]:
            temp_list = []
            for num in range(num_iter):
                temp_list.append(self.get_tile(tile[0] + offset[0] * num, tile[1] + offset[1] * num))
            merged_list = merge(temp_list)
            for num in range(num_iter):
                old_value = self.get_tile(tile[0] + offset[0] * num, tile[1] + offset[1] * num)
                self.set_tile(tile[0] + offset[0] * num, tile[1] + offset[1] * num, merged_list[num])
                if old_value != merged_list[num]:
                    changed = True
        if changed:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        row = random.randint(0, self.grid_height - 1)
        col = random.randint(0, self.grid_width - 1)
        while self.get_tile(row, col) != 0:
            row = random.randint(0, self.grid_height - 1)
            col = random.randint(0, self.grid_width - 1)
        if random.random() < 0.9:
            self.set_tile(row, col, 2)
        else:
            self.set_tile(row, col, 4)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(5, 4))
