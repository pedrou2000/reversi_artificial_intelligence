# Author: Pedro Urbina Rodriguez


from __future__ import annotations  # For Python 3.7

# import from parent directory
import os, sys
parent = os.path.abspath('.')
sys.path.insert(1, parent)


import numpy as np
import time

from game_infrastructure.game import Player, TwoPlayerGameState, TwoPlayerMatch
from heuristic import simple_evaluation_function
from game_infrastructure.tictactoe import TicTacToe
from game_infrastructure.tournament import StudentHeuristic, Tournament

from heuristic import *
from game_infrastructure.reversi import (
    Reversi,
    from_array_to_dictionary_board,
    from_dictionary_to_array_board,
)



###############################################################################################
############################### HEURISTIC CLASSES #############################################
###############################################################################################
# Classes for executing the strategies developed in heuristic.py. See this file for an 
# explanation of the heuristics.

class HeuristicDummy(StudentHeuristic):

    def get_name(self) -> str:
        return "dummy"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        # Use an auxiliary function.
        return self.dummy(123)

    def dummy(self, n: int) -> int:
        return n + 4

class HeuristicRandom(StudentHeuristic):

    def get_name(self) -> str:
        return "random"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return float(np.random.rand())

class HeuristicSimpleEval(StudentHeuristic):

    def get_name(self) -> str:
        return "heuristic_1"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return simple_evaluation_function(state)

class HeuristicSimpleEval2(Heuristic):
    def get_name(self) -> str:
        return "heuristic_1"

    def evaluate(state: TwoPlayerGameState) -> float:
        return simple_evaluation_function(state)

class HeuristicEndGame(StudentHeuristic):
    """Heuristic using result_end_game evaluation function"""

    def get_name(self) -> str:
        return "HeuristicEndGame"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return result_end_game(state)

class HeuristicMaxCaptureblePieces(StudentHeuristic):
    """Heuristic using maximize_possibly_captured_pieces evaluation function"""

    def get_name(self) -> str:
        return "HeuristicMaxCaptureblePieces"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return maximize_possibly_captured_pieces(state)

class HeuristicBestCapture(StudentHeuristic):
    """Heuristic using maximize_captured_piece evaluation function"""

    def get_name(self) -> str:
        return "HeuristicBestCapture"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return maximize_captured_piece(state)

class HeuristicCorners(StudentHeuristic):
    """HeuristicCorners"""
    
    def get_name(self) -> str:
        return "HeuristicCorners"
        
    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        return corners_based_function(state)

class HeuristicPonderationMax(StudentHeuristic):
    """Heuristic using ponderation_maximize evaluation function.
    Combines HeuristicEndGame, HeuristicMaxCapturablePieces, HeuristicBestCapture 
    and corners_based_function in an efficient way"""

    def get_name(self) -> str:
        return "HeuristicPonderationMax"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        p_actual = 0.2
        p_max_captured = 0.1
        p_sum_captured = 0.3
        p_corners = 0.4
        return ponderation_maximize(state, p_actual, p_max_captured, p_sum_captured, p_corners)
        
class HeuristicParityMobilityCorners1(StudentHeuristic):
    """ Combines corners_based_function, parity_function and best_mobility_function
    with some optimized poderations"""

    def get_name(self) -> str:
        return "HeuristicParityMobilityCorners1"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        functions = [corners_based_function, parity_function, best_mobility_function]
        weights = [0.3, 0.3, 0.4]
        
        return combined_based_function(state, functions, weights)
        
class HeuristicParityMobilityCorners2(StudentHeuristic):
    """ Combines corners_based_function, parity_function and best_mobility_function
    with some optimized poderations"""

    def get_name(self) -> str:
        return "HeuristicParityMobilityCorners2"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        functions = [corners_based_function, parity_function, best_mobility_function]
        weights = [0.7, 0.1, 0.2]
        
        return combined_based_function(state, functions, weights)



###############################################################################################
############################### TOURNAMENT CONFIGURATION ######################################
###############################################################################################

# Possible Initial States
intermediate_state_small = (
    [
        '..B.B..',
        '.WBBW..',
        'WBWBB..',
        '.W.WWW.',
        '.BBWBWB',
    ]
)

initial_state = (
    [
        '........',
        '........',
        '........',
        '...WB...',
        '...BW...',
        '........',
        '........',
        '........'
    ]
)

intermediate_state_large = (
    [
        '........',
        '...B.B..',
        '..WBBW..',
        '.WBWBB..',
        '..W.WWW.',
        '..BBWBWB',
        '........',
        '........'
    ]
)

initial_board_global = intermediate_state_small

repetitions = 1 # tournament repetitions
depth = 2 # search depth used by the search algorithms
max_sec_per_move = 5

# different tournament moddalities can be selected
test = 0 # normal tournament
#test = 1 # only one heuristic tested against others (tested_against_heuristics)
#test = 2 # optimize one heuristic's ponderations

# here we choose the players (herusitic classes) which will play against each other in case of normal tournament
strats = {'End': [HeuristicPonderationMax], 'EndMaxBest': [HeuristicParityMobilityCorners1]}

# this varibles are used in one_heuristic_against_others, when not running a normal tournament
tested_heuristic = {'0': [HeuristicPonderationMax]}
tested_against_heuristics = {'1': [HeuristicParityMobilityCorners1]}#, '2': [HeuristicParityMobilityCorners2]}




###############################################################################################
#################################### TOURNAMENT RUN ###########################################
###############################################################################################

def one_heuristic_against_others(ponderations: bool):
    """This function runs tournaments confronting the heuristic in the tested_heuristic 
    dictionary against all the heuristics in the tested_against_heuristics dictionaty"""

    scores_backup = []

    # for each heuristic in tested_against_heuristics a tournament
    for heuristic_key in tested_against_heuristics.items():
        strats = tested_heuristic.copy()
        strats.update([heuristic_key])

        scores, totals, names = tour.run(
            student_strategies=strats,
            increasing_depth=False,
            n_pairs=repetitions,
            allow_selfmatch=False,
        )
        # we save the relevant results of the tournament in scores_backup
        tested_heuristic_wins = list(list(scores.values())[0].values())[0]
        tested_against_name = list(names.values())[1]
        scores_backup.append([tested_against_name, tested_heuristic_wins])

    # print results
    tested_heuristic_name = list(names.values())[0]
    print()
    print()
    print('FINAL RESULTS')
    print('Tested heuristic: ' + tested_heuristic_name)
    print('[won_games : against_heuristic]')
    final_won = 0
    for result in scores_backup:
        final_won += result[1]
        print('[%d / %d : ' %(result[1], repetitions*2) + result[0] + ']')
    
    if ponderations:
        print('You heurisitc with ponderations: %.2f, %.2f, %.2f has won: %d' %(i,j,k,final_won))
    else:
        print('You heurisitc has won: %d' %final_won)
        

def create_match(player1: Player, player2: Player) -> TwoPlayerMatch:
    """Function to create a match between 2 players."""

    initial_board = initial_board_global

    if initial_board is None:
        height, width = 8, 8  
    else:
        height = len(initial_board)
        width = len(initial_board[0])
        try:
            initial_board = from_array_to_dictionary_board(initial_board)
        except ValueError:
            raise ValueError('Wrong configuration of the board')
    
    game = Reversi(
        player1=player1,
        player2=player2,
        height=height,
        width=width,
    )
    
    initial_player = player1
    game_state = TwoPlayerGameState(
        game=game,
        board=initial_board,
        initial_player=initial_player,
    )

    return TwoPlayerMatch(game_state, max_sec_per_move=max_sec_per_move, gui=False)

tour = Tournament(max_depth=depth, init_match=create_match)




# print information about the tournaments that will be run
print()
print('Playing with depth %d. Initial Board:' %(depth))
print(*initial_board_global, sep = "\n")
print()
print(
    'Results for tournament where each game is repeated '
    + '%d (%d x 2) times, alternating colors for each player' % (2 * repetitions, repetitions),
)
print()



# depending on the value of the test variable different ways of confronting heuristics will be used
# if test equals 0 a normal tournament in which each heuristic face the rest will be carried out
if test == 0 :
    ##### NORMAL TOURNAMENT #####
    print('NORMAL TOURNAMENT')

    start = time.time()
    scores, totals, names = tour.run(
        student_strategies=strats,
        increasing_depth=False,
        n_pairs=repetitions,
        allow_selfmatch=False,
    )
    print('Execution time: %s' %(time.time() - start))
    print()
    print('\ttotal:', end='')
    for name1 in names:
        print('\t%s' % (name1), end='')
    print()
    for name1 in names:
        print('%s\t%d:' % (name1, totals[name1]), end='')
        for name2 in names:
            if name1 == name2:
                print('\t---', end='')
            else:
                print('\t%d' % (scores[name1][name2]), end='')
        print()

# if test equals 1 a tournament in which one heuristic is faced against a list of others will be
# carried out
elif test == 1:
    ##### TESTING A SINGLE HEURISTIC AGAINST OTHERS #####
    print('TESTING A SINGLE HEURISTIC AGAINST OTHERS')

    one_heuristic_against_others(ponderations = False)

# if test equals 2 a tournament in which a combined function will be faced against a list of
# others will be carried out. This time the weights given to each of the evaluation functions
# that constitute the combined one, will be changing to obtain the best combination of weights.

# Some lines of the code are commented because they were used to maximize a combined function
# that combines four evaluation functions instead of three.
elif test == 2:
    ##### TRYING DIFFERENT PONDERATIONS FOR A GIVEN HEURISTIC #####
    print('TRYING DIFFERENT PONDERATIONS FOR A GIVEN HEURISTIC')

    #ponderation_list = [num * 0.10 for num in range(10)]
    ponderation_list = [0.1, 0.2, 0.3, 0.4]
    
    for i in ponderation_list:
        for j in ponderation_list:
            #for k in ponderation_list:
            if (i + j) <= 1:
                k = 1 - j - i
                #if (i + j + k) <= 1:
                    #z = 1 - (i + j + k)
                    
                """ For each of the ponderations in the ponderation list we define a class
                in order to test how this class would work, and then we test it """
                class HeuristicToMaximize(StudentHeuristic):
                    def get_name(self) -> str:
                        return "HeuristicToMaximize"

                    def evaluation_function(self, state: TwoPlayerGameState) -> float:
                        functions = [corners_based_function, parity_function, best_mobility_function]
                        weights = [i, j, k]
        
                        return combined_based_function(state, functions, weights)
                        #return ponderation_maximize(state, i, j, k, z)
                
                tested_heuristic = {'0': [HeuristicToMaximize]}

                one_heuristic_against_others(ponderations = True)
