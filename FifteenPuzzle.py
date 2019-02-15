"""
Loyd's Fifteen puzzle - solver and visualizer

Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui


def move_down(current_target_row, target_row):
    """
    Move the target tile to the down.
    """

    return "druld" * (target_row - current_target_row)


def moves_lr(times, current_target_row, target_row):
    """
    Move the target tile to the left or right.
    """

    solved = ""

    # move_left --> Current_target[0] on the right
    # must move to the left.
    if times < 0:
        # rest
        if current_target_row > 0:
            solved += "ulldr" * abs(times)
            solved += "ulld"
        # first row
        else:
            solved += "dllur" * abs(times)
            solved += "dllu"

    # move_right --> Current_target[0] on the left
    # must move to the right
    elif times > 0:
        # rest
        if current_target_row > 0:
            solved += "urrdl" * abs(times)
        # first row
        else:
            solved += "drrul" * abs(times)

    return solved


def position_tile(current_pos, desired_pos):
    """
    Position the target tile on the desired location.
    """

    # while moving the target tile to the target position
    move = ""
    current_pos_updated = list(current_pos)

    # move up
    if desired_pos[1] == current_pos[1]:
        move += "u" * (desired_pos[0] - current_pos_updated[0] - 1)
        move += "lu"

    else:
        # first up
        move += "u" * (desired_pos[0] - current_pos[0])

        # move left
        if desired_pos[1] > current_pos[1]:
            move += "l" * (desired_pos[1] - current_pos[1])
            current_pos_updated[1] = current_pos[1] + 1

        # move right
        elif desired_pos[1] < current_pos[1]:
            move += "r" * abs(desired_pos[1] - current_pos[1])
            current_pos_updated[1] = current_pos[1] - 1

            # reposition tile zero on the left of the target
            if desired_pos[1] - current_pos_updated[1] == 0:
                if current_pos_updated[0] != 0:
                    move += "ulld"
                else:
                    move += "dllu"

    move += moves_lr(desired_pos[1] - current_pos_updated[1], current_pos_updated[0], desired_pos[0])
    move += move_down(current_pos_updated[0], desired_pos[0])

    return move


class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """

        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """

        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"

        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """

        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """

        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """

        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """

        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """

        new_puzzle = Puzzle(self._height, self._width, self._grid)

        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """

        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)

        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """

        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """

        # Tile zero is positioned at (i,j).
        if self.get_number(target_row, target_col) != 0:
            print("lower_row_invariant: target is not zero")
            return False

        # All tiles in rows i+1 or below are positioned at their solved location.
        for row in range(target_row + 1, self._height):
            for col in range(self._width):
                if col + self._width * row != self.get_number(row, col):
                    print("lower_row_invariant: below rows incorrect")
                    return False

        # All tiles in row i to the right of position (i,j)
        # are positioned at their solved location. 
        for col in range(target_col + 1, self._width):
            if col + self._width * target_row != self.get_number(target_row, col):
                print("lower_row_invariant: current row incorrect")
                return False

        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """

        assert target_row > 1 and target_col > 0, "solve_interior_tile: indexes out of range"

        # find the current position of the tile that should appear at this position
        current_pos = self.current_position(target_row, target_col)

        assert current_pos[0] < target_row or (current_pos[0] == target_row and current_pos[
            1] < target_col), "solve_interior_tile: target indexes incorrect"

        move = position_tile(current_pos, (target_row, target_col))

        self.update_puzzle(move)

        return move

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """

        assert target_row > 1, "solve_col0_tile: index out of range"

        move = ""

        # move the zero tile from (i,0) to (i−1,1)
        start_move = "ur"
        self.update_puzzle(start_move)

        current_pos = self.current_position(target_row, 0)

        # if the target tile is not now at position (i,0)
        if (target_row, 0) != current_pos:
            # reposition the target tile to position (i−1,1)
            # and the zero tile to position (i−1,0)
            move += position_tile(current_pos, (target_row - 1, 1))

            # apply the fixed move string
            fixed_move = "ruldrdlurdluurddlur"

            move += fixed_move

        # conclude by moving tile zero to the right end of row i−1
        final_move = "r" * (self.get_width() - 2)

        self.update_puzzle(move + final_move)

        return start_move + move + final_move

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """

        # tile zero is at (0,j)
        if self.get_number(0, target_col) != 0:
            print("row0_invariant: target is not zero")
            return False

        # check all positions at the right
        for idx_i in range(2):
            for idx_j in range(target_col + 1, self.get_width()):
                if (idx_i, idx_j) != self.current_position(idx_i, idx_j):
                    print("row1_invariant: (%d,%d) index fail" % (idx_i, idx_j))
                    return False

        # all positions either below or to the right of this position are solved
        # additionally checks whether position (1,j) is also solved
        for row in range(2, self._height):
            for col in range(self._width):
                if (row, col) != self.current_position(row, col):
                    print("row0_invariant: below rows incorrect")
                    return False

        # check position below tile zero
        if (1, target_col) != self.current_position(1, target_col):
            print("row0_invariant: current row incorrect")
            return False

        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """

        # tile zero is at (1,j)
        if self.get_number(1, target_col) != 0:
            print("row1_invariant: target is not zero")
            return False

        # check all positions at the right
        for idx in range(target_col + 1, self.get_width()):
            if (0, idx) != self.current_position(0, idx):
                print("row1_invariant: (0,%d) index fail" % idx)
                return False

        # all positions either below or to the right of this position are solved
        if not self.lower_row_invariant(1, target_col):
            print("row1_invariant: lower_row_invariant not passed")
            return False

        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """

        move = ""

        # move the zero tile from position (0,j) to (1,j−1)
        start_move = "ld"
        self.update_puzzle(start_move)

        current_pos = self.current_position(0, target_col)

        assert self.current_position(0, 0) == (1, target_col - 1), "solve_row0_tile: tile zero not well positioned"

        # if the target tile is not now at position (0,j)
        if (0, target_col) != current_pos:
            # reposition the target tile to position (1,j−1)
            # with tile zero in position (1,j−2)
            move += position_tile(current_pos, (1, target_col - 1))

            # apply the fixed move string
            fixed_move = "urdlurrdluldrruld"

            move += fixed_move

        self.update_puzzle(move)

        return start_move + move

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """

        move = ""

        assert self.current_position(0, 0) == (1, target_col), "solve_row0_tile: tile zero not well positioned"

        current_pos = self.current_position(1, target_col)

        # solve the position
        move += position_tile(current_pos, (1, target_col))

        # reposition tile zero from (1,j) to (0, j + 1)
        final_move = "ur"

        self.update_puzzle(move + final_move)

        return move + final_move

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """

        fixed_move = "rdlu"
        total_move = ""
        move = ""
        counter = 0

        # check and put zero tile in (0,0) if not
        if self.current_position(0, 0) == (0, 1):
            move = "l"
            self.update_puzzle(move)

            total_move += move
        elif self.current_position(0, 0) == (1, 0):
            move = "u"
            self.update_puzzle(move)

            total_move += move
        elif self.current_position(0, 0) == (1, 1):
            move = "ul"
            self.update_puzzle(move)

            total_move += move

        # turn
        indexes = [(idx_i, idx_j) for idx_i in range(2) for idx_j in range(2)]
        cond = [(self.get_number(idx[0], idx[1]) == idx[1] + self._width * idx[0]) for idx in indexes]

        while False in cond and counter < 7:
            self.update_puzzle(fixed_move)

            total_move += fixed_move

            cond = [(self.get_number(idx[0], idx[1]) == idx[1] + self._width * idx[0]) for idx in indexes]

            counter += 1

        if counter == 7:
            return ""
        else:
            return total_move

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """

        move = ""

        # move tile zero to last tile
        current_pos = self.current_position(0, 0)

        move += "d" * ((self.get_height() - 1) - current_pos[0])
        move += "r" * ((self.get_width() - 1) - current_pos[1])

        self.update_puzzle(move)

        # last n - 2 rows
        aux_heigth = range(2, self.get_height())
        aux_heigth = reversed(aux_heigth)
        aux_width = range(self.get_width())
        aux_width = reversed(aux_width)

        for idx_i in aux_heigth:
            for idx_j in aux_width:
                self.lower_row_invariant(idx_i, idx_j)

                if idx_j == 0:
                    move += self.solve_col0_tile(idx_i)
                else:
                    move += self.solve_interior_tile(idx_i, idx_j)

        # last m - 2 cols
        aux_width = range(2, self.get_width())
        aux_width = reversed(aux_width)

        for idx_j in aux_width:
            self.row1_invariant(idx_j)
            move += self.solve_row1_tile(idx_j)
            self.row0_invariant(idx_j)
            move += self.solve_row0_tile(idx_j)

        # solve 2 x 2 square
        move += self.solve_2x2()

        return move


# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]]))
