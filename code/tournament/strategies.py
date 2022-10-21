# Author: Pedro Urbina Rodríguez

from __future__ import (
    annotations,
)
from game import (
    TwoPlayerGameState,
)
from reversi_artificial_intelligence.code.game_infrastructure.tournament import (
    StudentHeuristic,
)
from typing import (
    Callable, Sequence
)
from reversi import (
    Reversi,
)
import numpy as np


#Auxiliar functions

def result_end_game(state: TwoPlayerGameState) -> float:
    """Return game result as if game ended in this state."""
    state_value = 0
    scores = state.scores

    assert isinstance(scores, (Sequence, np.ndarray))
    score_difference = scores[0] - scores[1]

    if state.is_player_max(state.player1):
        state_value = score_difference
        
    elif state.is_player_max(state.player2):
        state_value = - score_difference

    else:
        raise ValueError('Player MAX not defined')

    return state_value

def combined_based_function(state: TwoPlayerGameState, functions, weights) -> float:
    """Auxiliary function used to give a ponderation of the input evaluation functions."""
    state_value = 0
    
    if len(functions) != len(weights):
        return state_value
    
    elif state.end_of_game:
        state_value = result_end_game(state)

    else:
        state_values = []
        for function in functions:
            state_values.append(function(state))
        
        for (weight, state_value_aux) in zip(weights, state_values):
           state_value = state_value + weight * state_value_aux
            
    return state_value
    
def ponderation_maximize(state: TwoPlayerGameState, p_actual, p_max_captured, p_sum_captured, p_corners) -> float:
    """This function returns an efficient ponderation of result_end_game, maximize_captured_piece, 
    maximize_possibly_captured_pieces and corners_based_function."""    
    state_value = 0
    actual_score = result_end_game(state)

    if state.end_of_game:
        state_value = actual_score

    else:
        # scores[0] => scores player1, scores[1] => scores player2
        successors = state.game.generate_successors(state)        
        corners_score = corners_based_function(state)
        score_maximum_captured = 0
        score_possibly_captured = 0

        if state.is_player_max(state.player1):
            for successor in successors:
                score_maximum_captured = max(score_maximum_captured, (successor.scores[0] - successor.scores[1]) - actual_score)
                score_possibly_captured += ((successor.scores[0] - successor.scores[1]) - actual_score)

        elif state.is_player_max(state.player2):
            for successor in successors:
                score_maximum_captured = max(score_maximum_captured, (successor.scores[1] - successor.scores[0])- actual_score)
                score_possibly_captured += ((successor.scores[1] - successor.scores[0]) - actual_score)

        else:
            raise ValueError('Player MAX not defined')

        # final ponderation of the calculated scores
        state_value = actual_score * p_actual + score_maximum_captured * p_max_captured + score_possibly_captured * p_sum_captured + corners_score * p_corners

    return state_value


def corners_based_function(state: TwoPlayerGameState) -> float:
    """Measures the difference in the number of corners captured."""
    state_value = 0
    
    if state.end_of_game:
        state_value = result_end_game(state)
    
    else:
        height = state.game.height
        width = state.game.width
        corners = [state.board.get((1, 1)), state.board.get((1, width)), state.board.get((height, 1)), state.board.get((height, width))]
    
        label_player1 = state.game.player1.label
        label_player2 = state.game.player2.label
        score = 0
        
        corners_count_player1 = corners.count(label_player1)
        corners_count_player2 = corners.count(label_player2)
        
        if (corners_count_player1 + corners_count_player2) != 0:
            score = 100  * (corners_count_player1 - corners_count_player2)/(corners_count_player1 + corners_count_player2)
        
        if state.is_player_max(state.player1):
            state_value = score
            
        elif state.is_player_max(state.player2):
            state_value = -score
    
    return state_value

def parity_function(state: TwoPlayerGameState) -> float:
    """Measures how well the player is doing in respect to the actual score."""
    state_value = 0
    
    if state.end_of_game:
        state_value = result_end_game(state)
        
    else:        
        player1_score = state.scores[0]
        player2_score = state.scores[1]
        
        score = 100 * (player1_score - player2_score)/(player1_score + player2_score)
        
        if state.is_player_max(state.player1):
            state_value = score
        
        elif state.is_player_max(state.player2):
            state_value = -score
        
    return state_value

def best_mobility_function(state: TwoPlayerGameState) -> float:
    """Returns the percentage of the player valid moves over all the valid moves that both 
    players could do."""
   
    if state.end_of_game:
        state_value = result_end_game(state)

    else:
        label_player1 = state.game.player1.label
        label_player2 = state.game.player2.label
        
        player1_valid_moves = state.game._get_valid_moves(state.board, label_player1)
        player2_valid_moves = state.game._get_valid_moves(state.board, label_player2)
            
        score = 0
                
        number_player1_valid_moves = len(player1_valid_moves)
        number_player2_valid_moves = len(player2_valid_moves)
            
        if ((number_player1_valid_moves + number_player2_valid_moves) != 0):
            score = 100 * (number_player1_valid_moves - number_player2_valid_moves)/(number_player1_valid_moves + number_player2_valid_moves)
                
        if state.is_player_max(state.player1):
            state_value = score
        elif state.is_player_max(state.player2):
            state_value = -score
                
    return state_value


class MySolution1 (StudentHeuristic):
    """ Combines corners_based_function, parity_function and best_mobility_function
    with some optimized poderations"""

    def get_name(self) -> str:
        return "2351_9_ParityMobilityCorners1"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        functions = [corners_based_function, parity_function, best_mobility_function]
        weights = [0.3, 0.3, 0.4]
        
        return combined_based_function(state, functions, weights)
        
        
        
class MySolution2 (StudentHeuristic):
    """Heuristic using ponderation_maximize evaluation function.
    Combines HeuristicEndGame, HeuristicMaxCapturablePieces, HeuristicBestCapture 
    and corners_based_function in an efficient way"""

    def get_name(self) -> str:
        return "2351_9_PonderationMax"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        p_actual = 0.2
        p_max_captured = 0.1
        p_sum_captured = 0.3
        p_corners = 0.4
        return ponderation_maximize(state, p_actual, p_max_captured, p_sum_captured, p_corners)



class MySolution3 (StudentHeuristic):
    """ Combines corners_based_function, parity_function and best_mobility_function
    with some optimized poderations"""

    def get_name(self) -> str:
        return "2351_9_ParityMobilityCorners2"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        functions = [corners_based_function, parity_function, best_mobility_function]
        weights = [0.7, 0.1, 0.2]
        
        return combined_based_function(state, functions, weights)
