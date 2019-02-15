"""
Solitaire version of Mancala - Tchoukaillon

Goal: Move as many seeds from given houses into the store
"""

import poc_mancala_testsuite
import poc_mancala_gui


class SolitaireMancala:
    """
    Simple class that implements Solitaire Mancala
    """

    def __init__(self):
        """
        Create Mancala game with empty store and no houses
        """
        self._board = [0]

    def set_board(self, configuration):
        """
        Take the list configuration of initial number of seeds for given houses
        house zero corresponds to the store and is on right
        houses are number in ascending order from right to left
        """
        self._board = list(configuration)

    def __str__(self):
        """
        Return string representation for Mancala board
        """
        self._board.reverse()
        board_str = str(self._board)
        self._board.reverse()
        return board_str

    def get_num_seeds(self, house_num):
        """
        Return the number of seeds in given house on board
        """
        return self._board[house_num]

    def is_game_won(self):
        """
        Check to see if all houses but house zero are empty
        """
        for idx in range(1, len(self._board)):
            if self._board[idx] != 0:
                return False
        return True

    def is_legal_move(self, house_num):
        """
        Check whether a given move is legal
        """
        if house_num == 0:
            return False
        else:
            return house_num == self._board[house_num]

    def apply_move(self, house_num):
        """
        Move all of the stones from house to lower/left houses
        Last seed must be played in the store (house zero)
        """
        if self.is_legal_move(house_num):
            self._board[house_num] = 0
            for idx in range(house_num - 1, -1, -1):
                self._board[idx] += 1

    def choose_move(self):
        """
        Return the house for the next shortest legal move
        Shortest means legal move from house closest to store
        Note that using a longer legal move would make smaller illegal
        If no legal move, return house zero
        """
        for idx in range(1, len(self._board)):
            if self.is_legal_move(idx):
                return idx
        return 0

    def plan_moves(self):
        """
        Return sequence of shortest legal moves until none are available
        Not used in GUI version, only for machine testing
        """
        game = SolitaireMancala()
        game.set_board(self._board)
        moves = []
        while not game.is_game_won():
            move = game.choose_move()
            if move == 0:
                break
            else:
                game.apply_move(move)
                moves.append(move)
        return moves


poc_mancala_testsuite.run_test(SolitaireMancala)
poc_mancala_gui.run_gui(SolitaireMancala())
