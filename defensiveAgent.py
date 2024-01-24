import random

opponent_moves = dict()
def defensive_agent(obs, config):
    my_piece = obs.mark
    enemy_piece = 1 if my_piece == 2 else 2
    for i, cell in enumerate(obs.board):
        if cell != my_piece and cell != 0:
            opponent_moves[i] = opponent_moves.get(i, 0) + cell

    opponent_last_move = None
    for cell, mark in opponent_moves.items():
        if mark == enemy_piece:
            opponent_last_move = cell

    valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
    if opponent_last_move is None:
        return random.choice(valid_moves)

    retaliation_ideas = []
    if opponent_last_move + 1 < len(obs.board):
        if obs.board[opponent_last_move + 1] == 0:
            if (opponent_last_move + 1) + 7 < len(obs.board):
                if obs.board[(opponent_last_move + 1) + 7] != 0:
                    retaliation_ideas.append(opponent_last_move + 1)
            else:
                retaliation_ideas.append(opponent_last_move + 1)

    if opponent_last_move - 1 >= 0:
        if obs.board[opponent_last_move - 1] == 0:
            if (opponent_last_move - 1) + 7 < len(obs.board):
                if obs.board[(opponent_last_move - 1) + 7] != 0:
                    retaliation_ideas.append(opponent_last_move - 1)
            else:
                retaliation_ideas.append(opponent_last_move - 1)

    if opponent_last_move % 7 in valid_moves:
        retaliation_ideas.append(opponent_last_move)

    retaliation_ideas = [col % 7 for col in retaliation_ideas]
    valid_ideas = [cell for cell in retaliation_ideas if cell in valid_moves]
    if len(valid_ideas) == 0:
        return random.choice(valid_moves)

    return random.choice(valid_ideas)