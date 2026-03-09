# Step number one: creating the game constants : 

nodes = {} # infoset : nodes

class Node : 
    
    def __init__(self, history : str) -> None:
        self.strategy = [0.0] * 2
        self.strategy_sum = [0.0] * 2
        self.regret_sum = [0.0] * 2
        
        self.actions = {"Call": 0, "Fold" : 1} if history and history[-1] == 'b' else {"Bet" : 0, "Check" : 1}
        pass
    
    def get_strategy(self) :
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
            self.strategy_sum[key] += self.strategy[key]

            
        return self.strategy


def terminal(history):
    pass

def payoff (cards, history)->float :
    return 2.3
    pass


    
def cfr(cards, reach_p1, reach_p2, history) -> float:
    
    current_player = 1 if len(history) % 2 else 0
    
    if terminal(history):
        return payoff(cards, history)
    
    info_set = cards[current_player] + history
    
    if info_set not in nodes : 
        nodes[info_set] = Node(history)
    
    node : Node = nodes[info_set]
    strategy = node.get_strategy()
    
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
            action_values[a] = cfr(cards, strategy[a] * reach_p1, reach_p2, next_history)
        else :
            action_values[a] = cfr(cards, reach_p1, reach_p2 * strategy[a], next_history)
            
        node_value += strategy[a] * action_values[a]
        
    for action in node.actions : 
        a = node.actions[action]
        opponent_reach = reach_p2 if current_player == 0 else reach_p1
        node.regret_sum[a] += opponent_reach * (action_values[a] - node_value)
    
    return node_value


 