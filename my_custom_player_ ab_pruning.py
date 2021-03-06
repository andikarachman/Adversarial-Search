
from sample_players import DataPlayer
import random
from isolation import DebugState, Isolation


class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only *required* method. You can modify
    the interface for get_action by adding named parameters with default
    values, but the function MUST remain compatible with the default
    interface.

    **********************************************************************
    NOTES:
    - You should **ONLY** call methods defined on your agent class during
      search; do **NOT** add or call functions outside the player class.
      The isolation library wraps each method of this class to interrupt
      search when the time limit expires, but the wrapper only affects
      methods defined on this class.

    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.
    **********************************************************************
    """
    def get_action(self, state, depth_max=100):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller is responsible for
        cutting off the function after the search time limit has expired. 

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)
        #import random

        #self.queue.put(random.choice(state.actions()))
        '''if state.ply_count < 2:
            print(bin(state.board))
            print(state.locs)
            board = Isolation()
            debug_board = DebugState.from_state(state)
            print(debug_board)
        
        if state.ply_count < 2: 
            self.queue.put(random.choice(state.actions()))
            print(bin(state.board))
            print(state.locs)'''

        if state.ply_count < 2: 
            self.queue.put(random.choice(state.actions()))
        for dp in range(1, depth_max+1):
            self.queue.put(self.alpha_beta_search(state, depth=dp))
            

    def alpha_beta_search(self, state, depth):

        def min_value(state, alpha, beta, depth):
            if state.terminal_test(): 
                return state.utility(self.player_id)
            if depth <= 0: 
                return self.score(state)
    
            v = float("inf")
            for a in state.actions():
                v = min(v, max_value(state.result(a), alpha, beta, depth-1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        def max_value(state, alpha, beta, depth):
            if state.terminal_test(): 
                return state.utility(self.player_id)
            if depth <= 0: 
                return self.score(state)
    
            v = float("-inf")
            for a in state.actions():
                v = max(v, min_value(state.result(a), alpha, beta, depth-1))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        alpha = float("-inf")
        beta = float("inf")
        best_score = float("-inf")
        best_move = None
        for a in state.actions():
            v = min_value(state.result(a), alpha, beta, depth)
            alpha = max(alpha, v)
            if v > best_score:
                best_score = v
                best_move = a
        return best_move


    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)

