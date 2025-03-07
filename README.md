# Pac-Man AI: Deep Learning Agent

## Overview
This project implements a **Deep Learning-based AI** to play a **Pac-Man** game using **PyTorch**. The goal of the agent is to **survive as long as possible**, avoiding ghosts while collecting all available points in the maze. We chose **Deep Learning** over traditional Q-Learning due to the high-dimensional state space and the need for adaptive decision-making.

## Why Deep Learning Instead of Q-Learning?
Traditional **Q-Learning** struggles in environments with large state spaces and dynamic obstacles. Since Pac-Man requires strategic decision-making in a constantly changing environment, Deep Learning—particularly using **Deep Q-Networks (DQN)** or policy gradient methods—allows the agent to generalize across different scenarios, improving its ability to **dodge ghosts and maximize score efficiently**.

## Problem Statement
The agent must navigate the maze while:
- **Avoiding ghosts** to prevent losing.
- **Collecting all pellets** to maximize the score.
- **Using power pellets strategically** to temporarily hunt ghosts and gain extra points.
- **Making real-time decisions** in an unpredictable environment.

By training with Deep Learning, the agent learns **optimal behaviors** through reinforcement rather than relying on hardcoded rules.

## Link to video demonstration
[Video](https://drive.google.com/file/d/1dhmWJkM72wTe-DKnNEf0px-MPuQaXAnF/view?usp=sharing)


## Environment Setup
### Prerequisites

For this project we used **Python 3.12.3** and **Pygame 2.6.1**

Ensure you have installed the following dependencies:
```sh
pip install torch numpy matplotlib
```

### Clone Repository
```sh
git clone https://github.com/AlbertoMorales24/QLearningGame.git
cd QLearningGame
```

## Training the Agent
To train the agent using **Deep Reinforcement Learning**, run:
```sh
python src/train.py
```
This will initialize the neural network and start the training process, allowing the agent to learn by interacting with the Pac-Man environment.

## Running the Game
Once trained, you can test the AI by running:
```sh
python src/mainMenu.py
```
The trained agent will control Pac-Man and attempt to survive while maximizing points.


## Team Members
- [Alberto Morales](https://github.com/AlbertoMorales24)
- [Edgar Velazquez](https://github.com/WeroVlz)
- [Jorge Vargas](https://github.com/Jorgepro89)
- [Ivan Andrade](https://github.com/Ivan9888)
