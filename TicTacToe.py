"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 10000  # Number of trials to run
MCMATCH = 2.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player


# Add your functions here.

def mc_trial(board, player):
    """
    This function takes a current board and the next player to move.
    The function plays a game starting with the given player by making random moves, alternating between players.
    The function returns when the game is over.
    The modified board will contain the state of the game.
    """
    while board.check_win() is None:
        empty_squares = board.get_empty_squares()
        (row, col) = empty_squares[random.randint(0, len(empty_squares) - 1)]
        board.move(row, col, player)
        player = provided.switch_player(player)


def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores (a list of lists) with the same dimensions as the Tic-Tac-Toe board,
    a board from a completed game, and which player the machine player is.
    The function scores the completed board and updates the scores grid.
    """
    winner = board.check_win()
    dim = board.get_dim()
    if winner == player:
        for row in range(dim):
            for col in range(dim):
                square = board.square(row, col)
                if square == player:
                    scores[row][col] += MCMATCH
                elif square != provided.EMPTY:
                    scores[row][col] -= MCOTHER
    elif winner != provided.DRAW and winner is not None:
        for row in range(dim):
            for col in range(dim):
                square = board.square(row, col)
                if square == player:
                    scores[row][col] -= MCMATCH
                elif square != provided.EMPTY:
                    scores[row][col] += MCOTHER


def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores.
    The function finds all of the empty squares with the maximum score and randomly return one of them as a
    (row, column) tuple. It is an error to call this function with a board that has no empty squares
    (there is no possible next move).
    """
    empty_squares = board.get_empty_squares()
    if not empty_squares:
        return None
    else:
        max_score = None
        square = None
        for (row, col) in empty_squares:
            score = scores[row][col]
            if max_score is None or score > max_score:
                max_score = score
                square = (row, col)
    return square


def mc_move(board, player, trials):
    """
    This function takes a current board, which player the machine player is, and the number of trials to run.
    The function uses the Monte Carlo simulation to return a move for the machine player in the form of a
    (row, column) tuple.
    """
    dim = board.get_dim()
    scores = [[0 for dummycol in range(dim)] for dummyrow in range(dim)]
    for dummy in range(trials):
        current_board = board.clone()
        mc_trial(current_board, player)
        mc_update_scores(scores, current_board, player)
    return get_best_move(board, scores)


# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

provided.play_game(mc_move, NTRIALS, False)
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
