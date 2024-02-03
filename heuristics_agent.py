import numpy as np
import random

def get_heuristic(grid, mark, config):
    num_threes = count_windows(grid, 3, mark, config)
    num_fours = count_windows(grid, 4, mark, config)
    num_threes_opp = count_windows(grid, 3, mark%2+1, config)
    num_twos_opp = count_windows(grid, 2, mark%2+1, config)
    score = num_threes - 3e2*num_threes_opp - (-1*num_twos_opp) + 1e6*num_fours
    return score


# Helper function for get_heuristic: checks if window satisfies heuristic conditions
def check_window(window, num_discs, piece, config):
    return (window.count(piece) == num_discs and window.count(0) == config.inarow - num_discs)


# Helper function for get_heuristic: counts number of windows satisfying specified heuristic conditions
def count_windows(grid, num_discs, piece, config):
    num_windows = 0
    # horizontal
    for row in range(config.rows):
        for col in range(config.columns - (config.inarow - 1)):
            window = list(grid[row, col:col + config.inarow])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    # vertical
    for row in range(config.rows - (config.inarow - 1)):
        for col in range(config.columns):
            window = list(grid[row:row + config.inarow, col])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    # positive diagonal
    for row in range(config.rows - (config.inarow - 1)):
        for col in range(config.columns - (config.inarow - 1)):
            window = list(grid[range(row, row + config.inarow), range(col, col + config.inarow)])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    # negative diagonal
    for row in range(config.inarow - 1, config.rows):
        for col in range(config.columns - (config.inarow - 1)):
            window = list(grid[range(row, row - config.inarow, -1), range(col, col + config.inarow)])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    return num_windows


def simulate_dropping_piece(grid, move, rows, mark):
    next_grid = grid.copy()
    for row in range(rows - 1, -1, -1):
        if next_grid[row, move] == 0:
            next_grid[row, move] = mark
            break

    return next_grid

def heuristics_agent(obs, config):
    valid_moves = [move for move in range(config.columns) if obs.board[move] == 0]
    grid = np.asarray(obs.board).reshape(config.rows, config.columns)

    move_scores = []
    for move in valid_moves:
        move_scores.append(get_heuristic(simulate_dropping_piece(grid, move, config.rows, obs.mark), obs.mark, config))
    scores = dict(zip(valid_moves, move_scores))

    max_scores = [key for key in scores.keys() if scores[key] == max(scores.values())]

    return random.choice(max_scores)