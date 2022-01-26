from agent import DDQNAgent
from game_env import Game
from copy import deepcopy

# import os

# # def clearConsole():
# #     command = 'clear'
# #     if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
# #         command = 'cls'
# #     os.system(command)

# # clearConsole()


if __name__=='__main__':
    env = Game()
    n_game = 10000000
    agent = DDQNAgent(alpha=0.003, gamma=0.99, epsilon=0.5, 
                       input_dims=env.num_state, n_actions=env.num_action,
                       batch_size=32)
    
    scores = []
    
    eps_history = []
    
    for i in range(n_game):
        done = False
        score = 0
        observation = env.reset()
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done = env.step(action)
            score += reward
            agent.remember(observation, action, reward, observation_, done)
            agent.learn()
            
            observation = observation_
            
        eps_history.append(agent.epsilon)
        scores.append(score)
        
        print(f"\033[2K-- Episode {i} | Agent Reward: {score} | Avg Score 1: {sum(scores)/len(scores)}", end="\n")
        env.visualizeBoard()
        print("\033[H\033[J", end="")
        
        if i % 100000 == 0 and i != 0:
            agent.save_model(f"model/agent-{i}.h5")
            
        
            
    
    