"""Strategies for two player games.

   Authors:
        Fabiano Baroni <fabiano.baroni@uam.es>,
        Alejandro Bellogin <alejandro.bellogin@uam.es>
        Alberto Suárez <alberto.suarez@uam.es>
"""

from __future__ import annotations  # For Python 3.7

from abc import ABC, abstractmethod
from typing import List

import numpy as np

from game import TwoPlayerGame, TwoPlayerGameState
from heuristic import Heuristic


class Strategy(ABC):
    """Abstract base class for player's strategy."""

    def __init__(self, verbose: int = 0) -> None:
        """Initialize common attributes for all derived classes."""
        self.verbose = verbose

    @abstractmethod
    def next_move(
        self,
        state: TwoPlayerGameState,
        gui: bool = False,
    ) -> TwoPlayerGameState:
        """Compute next move."""

    def generate_successors(
        self,
        state: TwoPlayerGameState,
    ) -> List[TwoPlayerGameState]:
        """Generate state successors."""
        assert isinstance(state.game, TwoPlayerGame)
        successors = state.game.generate_successors(state)
        assert successors  # Error if list is empty
        return successors


class RandomStrategy(Strategy):
    """Strategy in which moves are selected uniformly at random."""

    def next_move(
        self,
        state: TwoPlayerGameState,
        gui: bool = False,
    ) -> TwoPlayerGameState:
        """Compute next move."""
        successors = self.generate_successors(state)
        return np.random.choice(successors)


class ManualStrategy(Strategy):
    """Strategy in which the player inputs a move."""

    def next_move(
        self,
        state: TwoPlayerGameState,
        gui: bool = False,
    ) -> TwoPlayerGameState:
        """Compute next move."""
        successors = self.generate_successors(state)

        assert isinstance(state.game, TwoPlayerGame)
        if gui:
            index_successor = state.game.graphical_input(state, successors)
        else:
            index_successor = state.game.manual_input(successors)

        next_state = successors[index_successor]

        if self.verbose > 0:
            print('My move is: {:s}'.format(str(next_state.move_code)))

        return next_state


class MinimaxStrategy(Strategy):
    """Minimax strategy."""

    calls_number = 0 # for computer independent measures

    def __init__(
        self,
        heuristic: Heuristic,
        max_depth_minimax: int,
        verbose: int = 0,
    ) -> None:
        """Initialize depth of the search & heuristic."""
        super().__init__(verbose)
        self.heuristic = heuristic
        self.max_depth_minimax = max_depth_minimax

    def next_move(
        self,
        state: TwoPlayerGameState,
        gui: bool = False,
    ) -> TwoPlayerGameState:
        """Compute next state in the game."""

        successors = self.generate_successors(state)

        minimax_value = -np.inf

        for successor in successors:
            if self.verbose > 1:
                print('{}: {}'.format(state.board, minimax_value))

            successor_minimax_value = self._min_value(
                successor,
                self.max_depth_minimax,
            )
            if (successor_minimax_value > minimax_value):
                minimax_value = successor_minimax_value
                next_state = successor

        if self.verbose > 0:
            if self.verbose > 1:
                print('\nGame state before move:\n')
                print(state.board)
                print()
            print('Minimax value = {:.2g}'.format(minimax_value))

        if self.verbose > 0:
            print('Total number of recursive calls: %d' %MinimaxStrategy.calls_number)
        
        return next_state

    def _min_value(
        self,
        state: TwoPlayerGameState,
        depth: int,
    ) -> float:

        MinimaxStrategy.calls_number += 1 # for computer independent measures

        """Min step of the minimax algorithm."""
        if state.end_of_game or depth == 0:
            minimax_value = self.heuristic.evaluate(state)

        else:
            minimax_value = np.inf

            successors = self.generate_successors(state)
            for successor in successors:
                if self.verbose > 1:
                    print('{}: {}'.format(state.board, minimax_value))

                successor_minimax_value = self._max_value(
                    successor, depth - 1,
                )
                if (successor_minimax_value < minimax_value):
                    minimax_value = successor_minimax_value

        if self.verbose > 1:
            print('{}: {}'.format(state.board, minimax_value))

        return minimax_value

    def _max_value(
        self,
        state: TwoPlayerGameState,
        depth: int,
    ) -> float:
        
        MinimaxStrategy.calls_number += 1 # for computer independent measures

        """Max step of the minimax algorithm."""
        if state.end_of_game or depth == 0:
            minimax_value = self.heuristic.evaluate(state)

        else:
            minimax_value = -np.inf

            successors = self.generate_successors(state)
            for successor in successors:
                if self.verbose > 1:
                    print('{}: {}'.format(state.board, minimax_value))

                successor_minimax_value = self._min_value(
                    successor, depth - 1,
                )
                if (successor_minimax_value > minimax_value):
                    minimax_value = successor_minimax_value

        if self.verbose > 1:
            print('{}: {}'.format(state.board, minimax_value))

        return minimax_value


class MinimaxAlphaBetaStrategy(Strategy):
    """Minimax alpha-beta strategy."""

    calls_number = 0 # for computer independent measures

    def __init__(
        self,
        heuristic: Heuristic,
        max_depth_minimax: int,
        verbose: int = 0,
    ) -> None:
        super().__init__(verbose)
        self.heuristic = heuristic
        self.max_depth_minimax = max_depth_minimax

    def next_move(
        self,
        state: TwoPlayerGameState,
        gui: bool = False,
    ) -> TwoPlayerGameState:
        """Compute next state in the game."""
        # Remember to write the removed prints
        successors = self.generate_successors(state)
        
        # Because MAX starts
        minimax_value = -np.inf
        
        alpha = -np.inf
        
        beta  = np.inf
        
        for successor in successors:
            if self.verbose > 1:
                print('{}: {}'.format(state.board, minimax_value))
                
            # Here we do MIN_VALUE()
            successor_minimax_value = self._min_value(
                successor,
                self.max_depth_minimax,
                alpha,
                beta,
            )
            
            # Here we select the maximum and the state
            if (successor_minimax_value > minimax_value):
                minimax_value = successor_minimax_value
                next_state = successor
                
        if self.verbose > 0:
            if self.verbose > 1:
                print('\nGame state before move:\n')
                print(state.board)
                print()
            print('Minimax value = {:.2g}'.format(minimax_value))
    
        if self.verbose > 0:
            print('Total number of recursive calls: %d' %MinimaxAlphaBetaStrategy.calls_number)
        
        return next_state

    def _min_value(
        self,
        state: TwoPlayerGameState,
        depth: int,
        alpha: float,
        beta: float,
    ) -> float:
        
        MinimaxAlphaBetaStrategy.calls_number += 1 # for computer independent measures

        """Min step of the minimax algorithm."""
        if state.end_of_game or depth == 0:
            minimax_value = self.heuristic.evaluate(state)
        
        else:
            minimax_value = np.inf
            
            successors = self.generate_successors(state)
            for successor in successors:
                if self.verbose > 1:
                    print('{}: {}'.format(state.board, minimax_value))

                successor_minimax_value = self._max_value(
                    successor, depth - 1, alpha, beta,
                )
                
                minimax_value = min(minimax_value, successor_minimax_value)
                
                # Pruning
                if (minimax_value <= alpha):
                    if self.verbose > 0:
                        print('Pruning!')
                    return minimax_value
                
                beta = min(beta, minimax_value)
                
                
        if self.verbose > 1:
            print('{}: {}'.format(state.board, minimax_value))
            
        return minimax_value


    def _max_value(
        self,
        state: TwoPlayerGameState,
        depth: int,
        alpha: float,
        beta: float,
    ) -> float:
        
        MinimaxAlphaBetaStrategy.calls_number += 1 # for computer independent measures

        """Max step of the minimax algorithm."""
        if state.end_of_game or depth == 0:
            minimax_value = self.heuristic.evaluate(state)
        
        else:
            minimax_value = -np.inf
            
            successors = self.generate_successors(state)
            for successor in successors:
                if self.verbose > 1:
                    print('{}: {}'.format(state.board, minimax_value))
                
                successor_minimax_value = self._min_value(
                    successor, depth - 1, alpha, beta,
                )
                
                minimax_value = max(minimax_value, successor_minimax_value)
                
                # Pruning
                if (minimax_value >= beta):
                    if self.verbose > 0:
                        print('Pruning!')
                    return minimax_value
                
                alpha = max(alpha, minimax_value)
                
        if self.verbose > 1:
            print('{}: {}'.format(state.board, minimax_value))
            
        return minimax_value