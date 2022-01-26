from agent import DDQNAgent
from game_env import Game
from copy import deepcopy
import time

import bz2
import pickle
import _pickle as cPickle
# ref: https://betterprogramming.pub/load-fast-load-big-with-compressed-pickles-5f311584507e
def compressed_pickle(title, data):
    with bz2.BZ2File("./" +title + '.pbz2', 'w') as f: 
        cPickle.dump(data, f)
# Load any compressed pickle file
def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = cPickle.load(data)
    return data
# Load training and testing data


if __name__=='__main__':
    env = Game()
    n_game = 250000
    agent1 = DDQNAgent(alpha=0.003, gamma=0.99, epsilon=0.8, 
                       input_dims=env.num_state, n_actions=env.num_action,
                       batch_size=32) # Agen mengisi O
    agent2 = DDQNAgent(alpha=0.003, gamma=0.99, epsilon=0.8, 
                    input_dims=env.num_state, n_actions=env.num_action,
                    batch_size=32) # Agen mengisi X
    
    scores = {
        1: [],
        2: []
    }
    
    eps_history = {
        1: [],
        2: []
    }
    
    end_board_history = []
    
    time_hist = []
    time_started = time.time()
    
    for i in range(n_game):
        start = time.time()
        ###
        done = False
        score1 = 0
        score2 = 0
        observation = env.reset()
        while not done:
            if env.round % 2 == 0:
                action = agent1.choose_action(observation)
                observation_, reward, done = env.step(action)
                score1 += reward
                agent1.remember(observation, action, reward, observation_, done)
                agent1.learn()
            else:
                action = agent2.choose_action(observation)
                observation_, reward, done = env.step(action)
                if reward == -100:
                    score2 = 0
                score2 += reward
                agent2.remember(observation, action, reward, observation_, done)
                agent2.learn()
            
            observation = observation_
            
        eps_history[1].append(agent1.epsilon)
        eps_history[2].append(agent2.epsilon)
        scores[1].append(score1)
        scores[2].append(score2)
        ###
        stop = time.time()
        if i % 5 == 0:
            time_delta = stop - start
            time_hist.append(time_delta)
            time_avg = sum(time_hist) / len(time_hist)
            started_print = time.strftime("%b %d %Y %H:%M:%S", time.gmtime(time_started))
            elapsed_now = time.strftime("%H:%M:%S", time.gmtime(time.time() - time_started))
            approx_time = time.strftime("%H:%M:%S", time.gmtime(time_avg * (n_game - i)))
        
        print(f"Time Started: {started_print}\t| {elapsed_now} <- {approx_time}", end="\n")
        print(f"-- Episode {i}\t| Agent Reward 1(O): {score1}\t 2(X): {score2}\t| Avg Score 1: {sum(scores[1])/len(scores[1])} 2: {sum(scores[2])/len(scores[2])}", end="\n")
        end_board_history.append(env.board)
        env.visualizeBoard()
        print("\033[H\033[J", end="")
        
        if i % 20000 == 0 and i != 0:
            agent1.save_model(f"model/agent1-{i}.h5")
            agent2.save_model(f"model/agent2-{i}.h5")
            
    compressed_pickle("model/scores_history", scores)
    compressed_pickle("model/eps_history", eps_history)
    compressed_pickle("model/end_board_history", end_board_history)
            
        
            
    
    