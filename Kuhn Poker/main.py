import random
import numpy as np
import matplotlib.pyplot as plt
'''
Next work :
need to define average strat
need to print out the results.
'''

nodes = {} # infoset : nodes
class Node : 
    
    def __init__(self, history : str) -> None:
        self.strategy = [0.0] * 2
        self.strategy_sum = [0.0] * 2
        self.regret_sum = [0.0] * 2
        
        self.actions = {"Call": 0, "Fold" : 1} if history and history[-1] == 'B' else {"Bet" : 0, "Check" : 1}
        pass
    
    def get_strategy(self, current_reach_prob : float) :
        total = 0
        positive_regrets = [0.0] * 2
        for _, key in self.actions.items() :
            positive_regrets[key] = max(self.regret_sum[key], 0)
            total += positive_regrets[key]
        
        if total > 0 : 
            self.strategy = [x / total for x in positive_regrets]
        else : 
            self.strategy = [1 / len(self.actions)] * len(self.actions)
        
        for _, key in self.actions.items() : 
            self.strategy_sum[key] += current_reach_prob * self.strategy[key]

            
        return self.strategy
    
    def avg_strat(self):
        su = sum(self.strategy_sum)
        return [x/su for x in self.strategy_sum]

def terminal(history : str) -> bool:
    
    # Here, we need to check if the history is terminal or not.
    # Assuming history is a string, we need to check for patterns. 
    
    return history.endswith(("UU", "BF", "BC"))  

def hand_checker(a: str, b: str) -> int:
    
    rank = {"K": 3, "Q": 2, "J": 1}
    
    return 1 if rank[a] > rank[b] else 0
    
def payoff (cards : list[str], history : str) :
    a = cards[0]
    b = cards[1]
    if history.endswith("UU") : 
        if hand_checker(a, b) : return 1
        else : return -1
    elif history.endswith("BC") : 
        if hand_checker(a, b) : return 2
        else : return -2
    elif history.endswith("BF") : 
        if len(history) == 2 : return 1
        else : return -1
    return 0
    
def cfr(cards : list[str], reach_p0, reach_p1, history) -> float:
    
    # we are always assuming player 1 to be acting first.
    current_player = 1 if len(history) % 2 else 0
    
    if terminal(history):
        p = payoff(cards, history)
        return p 
    
    info_set = cards[current_player] + history
    
    if info_set not in nodes : 
        nodes[info_set] = Node(history)
    
    node : Node = nodes[info_set]
    curr_reach = reach_p0 if current_player == 0 else reach_p1
    strategy = node.get_strategy(curr_reach)
    
    action_values = [0.0] * 2
    node_value = 0 # this is basically the utility. 
    
    
    for action in node.actions:
        action_symbol = ''
        if action == "Call" : action_symbol = 'C'
        elif action == "Fold" : action_symbol = "F"
        elif action == "Check" : action_symbol = "U"
        else : action_symbol = "B"
        
        
        next_history = history + action_symbol
        a = node.actions[action]
        if current_player == 0 : 
            action_values[a] = -cfr(cards, strategy[a] * reach_p0, reach_p1, next_history)
        else :
            action_values[a] = -cfr(cards, reach_p0, reach_p1 * strategy[a], next_history)
            
        node_value += strategy[a] * action_values[a]
        
    for action in node.actions : 
        a = node.actions[action]
        opponent_reach = reach_p1 if current_player == 0 else reach_p0
        node.regret_sum[a] += opponent_reach * (action_values[a] - node_value)
    
    return node_value

def train():
    cards = ["K", "Q", "J"]

    track_Q = []
    track_J = []
    track_K = []
    track_K_check = []
    track_Q_check = []
    track_J_check = []

    for i in range(1, 165000):

        sample = random.sample(cards, len(cards))
        p1_card = sample[0]
        p2_card = sample[1]

        cfr([p1_card, p2_card], 1, 1, "")

        if(i % 1 == 0) : 
            if "Q" in nodes:
                strat = nodes["Q"].avg_strat()
                track_Q_check.append(strat[1])
                track_Q.append(strat[0])

            if "J" in nodes:
                strat = nodes["J"].avg_strat()
                track_J.append(strat[0])
                track_J_check.append(strat[1])

            if "K" in nodes:
                strat = nodes["K"].avg_strat()
                track_K_check.append(strat[1])
                track_K.append(strat[0])


    x = range(len(track_Q))
    
    plt.figure()
    plt.plot(smooth(track_K), label="K bet prob")
    plt.plot(smooth(track_Q), label="Q bet prob")
    plt.plot(smooth(track_J), label="J bet prob")
    plt.xlabel("Training steps")
    plt.ylabel("Bet Probability")
    plt.legend()
    plt.show()
    
    
    plt.figure()
    plt.plot(smooth(track_K_check), label="K check")
    plt.plot(smooth(track_Q_check), label="Q check")
    plt.plot(smooth(track_J_check), label="J check")
    plt.xlabel("Training steps")
    plt.ylabel("Check Probability")
    plt.legend()
    plt.show()
    
        
    # fig, ax = plt.subplots(1,2, figsize=(14,5))

    # ax1 = ax[0]
    # ax2 = ax[1]


    # ax1.plot(smooth(track_K), label="K bet prob")
    # ax1.plot(smooth(track_Q), label="Q bet prob")
    # ax1.plot(smooth(track_J), label="J bet prob")
    # ax1.set_xlabel("Training steps")
    # ax1.set_ylabel("Bet Probability")
    # ax1.legend()

    # ax2.plot(smooth(track_K_check), label="K check")
    # ax2.plot(smooth(track_Q_check), label="Q check")
    # ax2.plot(smooth(track_J_check), label="J check")
    # ax2.set_xlabel("Training steps")
    # ax2.set_ylabel("Check Probability")
    # ax2.legend()

    # plt.tight_layout()
    # plt.show()

def smooth(data, window=100):
    return np.convolve(data, np.ones(window)/window, mode='valid')

    

if __name__ == "__main__":
    train()