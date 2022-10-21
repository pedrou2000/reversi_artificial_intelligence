# Author: Pedro Urbina Rodriguez

from __future__ import annotations  # For Python 3.7
from typing import Callable, Sequence
from game_infrastructure.game import TwoPlayerGameState

import numpy as np
import copy

class Heuristic(object):
    """Encapsulation of the evaluation fucnction."""

    def __init__(
        self,
        name: str,
        evaluation_function: Callable[[TwoPlayerGameState], float],
    ) -> None:
        """Initialize name of heuristic & evaluation function."""
        self.name = name
        self.evaluation_function = evaluation_function

    def evaluate(self, state: TwoPlayerGameState) -> float:
        """Evaluate a state."""
        # Prevent modifications of the state.
        # Deep copy everything, except attributes related
        # to graphical display.
        state_copy = state.clone()
        return self.evaluation_function(state_copy)

    def get_name(self) -> str:
        """Name getter."""
        return self.name




###############################################################################################
############################### EVALUATION FUNCTIONNS #########################################
###############################################################################################

def simple_evaluation_function(state: TwoPlayerGameState) -> float:
    """Return a random value, except for terminal game states."""
    state_value = 2*np.random.rand() - 1
    if state.end_of_game:
        state_value = result_end_game(state)

    return state_value

def complex_evaluation_function(state: TwoPlayerGameState) -> float:
    """Return zero, except for terminal game states."""
    state_value = 0

    if state.end_of_game:
        state_value = result_end_game(state)

    else:
        successors = state.game.generate_successors(state)

        state_next = copy.deepcopy(state)
        state_next.next_player = state_next.game.opponent(
            state_next.next_player
        )
        successors_next = state.game.generate_successors(
            state_next
        )
        return len(successors_next) - len(successors)

    return state_value
     
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

def maximize_possibly_captured_pieces(state: TwoPlayerGameState) -> float:
    """Returns how many pieces could the player eat in his turn if he had unlimited moves."""
    state_value = 0
    actual_score = result_end_game(state)

    if state.end_of_game:
        state_value = actual_score        

    else:
        # scores[0] => scores player1, scores[1] => scores player2
        successors = state.game.generate_successors(state)
        
        if state.is_player_max(state.player1):
            for successor in successors:
                state_value += ((successor.scores[0] - successor.scores[1]) - actual_score) 
        elif state.is_player_max(state.player2):
            for successor in successors:
                state_value += ((successor.scores[1] - successor.scores[0]) - actual_score)
        else:
            raise ValueError('Player MAX not defined')

    return state_value

def maximize_captured_piece(state: TwoPlayerGameState) -> float:
    """Returns the maximum number of pieces that can be captured in the current state."""
    state_value = 0
    actual_score = result_end_game(state)

    if state.end_of_game:
        state_value = actual_score

    else:
        # scores[0] => scores player1, scores[1] => scores player2
        successors = state.game.generate_successors(state)
    
        if state.is_player_max(state.player1):
            for successor in successors:
                state_value = max(state_value, (successor.scores[0] - successor.scores[1]) - actual_score)
        elif state.is_player_max(state.player2):
            for successor in successors:
                state_value = max(state_value, (successor.scores[1] - successor.scores[0])- actual_score)
        else:
            raise ValueError('Player MAX not defined')

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
