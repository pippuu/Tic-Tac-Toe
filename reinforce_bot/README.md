# Creating BOT with DeepQLearning.  
\[Work In Progress\]

This bot is trained using `tensorflow-directml`. Where this version of tensorflow is `1.5`, so the API for creating this bot is maybe not supported when you already install the latest version of tensorflow.
  
## Recommendation and Contribution
Before you want try to tune this bot, we personally recommend you to downgrade to `python ver3.7` and use [virtual environment](https://docs.python.org/3/library/venv.html) for safe use. After that, install the requirements packages using `requirements.txt` file on this folder.   
   
You can fine tune:
1. The model on `agent.py`
2. How the environment react with agent action on `game_env.py`
3. How it train the model is train with the environment on `train.py`