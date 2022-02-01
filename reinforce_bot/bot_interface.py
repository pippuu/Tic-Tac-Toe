from copy import deepcopy
from tensorflow.keras.models import load_model
import numpy as np

class ReinforceBot:
    
    def __init__(self, player_num : int = 1, path=None):
        self.q_eval = None
        self.p_number = player_num
        if path != None:
            self.load_model(path)
        else:
            if player_num == 1:
                self.load_model("reinforce_bot/model/agentP1.h5")
            elif player_num == 2:
                # raise NotImplementedError("Work In Progress")
                self.load_model("reinforce_bot/model/agentP2.h5")
            else:
                raise TypeError("Not a valid player number")
        
    def action(self, board) -> int:
        board_copy = deepcopy(board)
        board_copy.append(self.p_number)
        valid_move = self._available_move(deepcopy(board_copy))
        state = np.array(board_copy)
        state = state[np.newaxis, :]
        actions = self.q_eval.predict(state)[0]
        pred = np.argsort(actions, kind='heapsort')[::-1]
        for i in pred:
            if i in valid_move:
                return i
    
    def _available_move(self,board) -> np.array:
        fin = []
        for i in range(len(board)):
            if board[i] == 0:
                fin.append(i)
        
        return np.array(fin)
    
    def load_model(self, path):
        self.q_eval = load_model(path)