from collections import deque
from datetime import datetime
import torch
import torch.optim as optim
import random
import numpy as np
from gameTraining import game
from DQN import DQN
from ReplayBuffer import ReplayBuffer
from trainSettings import hyperparamters

print(datetime.now())

# Hyperparameters
gamma = hyperparamters['gamma']
batch_size = hyperparamters['batch_size']
learning_rate = hyperparamters['learning_rate']
epsilon = hyperparamters['epsilon']
epsilon_min = hyperparamters['epsilon_min']
epsilon_decay = hyperparamters['epsilon_decay']
target_update_freq = hyperparamters['target_update_freq']
num_episodes = hyperparamters['num_episodes']
steps_per_episode = hyperparamters['steps_per_episode']

# Early stopping parameters
moving_avg_window = 50
reward_threshold = -10  # Stop training if moving avg reward is below this for too long
abort_after = 100  # Number of episodes to wait for improvement

# Initialize DQN
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
dqn = DQN().to(device)
target_dqn = DQN().to(device)
checkpoint_path = "pacman_dqn6.pth"  # Adjust the path if needed
try:
    #dqn.load_state_dict(torch.load(checkpoint_path, map_location=device))
    print(f"✅ Loaded pre-trained model from {checkpoint_path}")
except FileNotFoundError:
    print("🚫 No pre-trained model found. Starting from scratch.")
target_dqn.load_state_dict(dqn.state_dict())
target_dqn.eval()

optimizer = optim.Adam(dqn.parameters(), lr=learning_rate)
loss_fn = torch.nn.MSELoss()
replay_buffer = ReplayBuffer()

# Logging
reward_history = deque(maxlen=moving_avg_window)
best_moving_avg_reward = float('-inf')
no_improvement_counter = 0  # Counter for early stopping

def get_action(state):
    """Chooses an action using epsilon-greedy strategy."""
    global epsilon

    # Check if state is already a tensor
    if isinstance(state, np.ndarray):  # Convert only if it's a NumPy array
        state_tensor = torch.from_numpy(state).float().permute(2, 0, 1).unsqueeze(0).to(device)  # (1, 4, 10, 10)
    elif isinstance(state, torch.Tensor):  # If already a tensor, ensure correct shape
        if state.dim() == 3:  # (4, 10, 10) → Needs batch dimension
            state_tensor = state.unsqueeze(0).to(device)  # (1, 4, 10, 10)
        elif state.dim() == 4:  # (1, 4, 10, 10) → Already correct
            state_tensor = state.to(device)
        else:
            raise ValueError(f"Unexpected state shape: {state.shape}")  # Debugging

    if random.random() < epsilon:
        return random.choice([0, 1, 2, 3])  # Random action
    with torch.no_grad():
        q_values = dqn(state_tensor)  # Expecting (1, 4, 10, 10)
        return torch.argmax(q_values).item()  # Best action


# Training Loop
for episode in range(num_episodes):
    episode_data = game(500, 1, 1, 'S', steps_per_episode, get_action)  # Run game for N steps
    total_reward = sum(r for _, _, r, _, _ in episode_data)
    reward_history.append(total_reward)

    # Store experiences in buffer
    for state, action, reward, next_state, done in episode_data:
        replay_buffer.add(state, action, reward, next_state, done)

    # Train DQN if buffer has enough samples
    if replay_buffer.size() > batch_size:
        batch = replay_buffer.sample(batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.tensor(np.array(states), dtype=torch.float32).to(device)
        actions = torch.tensor(np.array(actions), dtype=torch.int64).to(device)
        rewards = torch.tensor(np.array(rewards), dtype=torch.float32).to(device)
        next_states = torch.tensor(np.array(next_states), dtype=torch.float32).to(device)
        dones = torch.tensor(np.array(dones), dtype=torch.float32).to(device)

        with torch.no_grad():
            max_next_q_values = target_dqn(next_states).max(1)[0]
            target_q_values = rewards + gamma * max_next_q_values * (1 - dones)

        q_values = dqn(states)
        q_values = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)

        loss = loss_fn(q_values, target_q_values)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    # Decay epsilon
    epsilon = max(epsilon_min, epsilon * epsilon_decay)

    # Update target network
    if episode % target_update_freq == 0:
        target_dqn.load_state_dict(dqn.state_dict())
    
    # Save a checkpoint every 200 episodes
    if episode % 200 == 0:
        torch.save(dqn.state_dict(), f"pacman_dqn8_checkpoint_{episode}.pth")
        print(f"Checkpoint saved at Episode {episode}")
        
    # Calculate moving average reward
    moving_avg_reward = np.mean(reward_history)

    # Check early stopping condition
    if moving_avg_reward > best_moving_avg_reward:
        best_moving_avg_reward = moving_avg_reward
        no_improvement_counter = 0
    else:
        no_improvement_counter += 1

    if no_improvement_counter >= abort_after and moving_avg_reward < reward_threshold:
        print(f"⚠️ Training aborted at episode {episode+1}: No improvement in {abort_after} episodes (Moving Avg Reward = {moving_avg_reward:.2f})")

    # Print progress every 10 episodes
    if episode % 10 == 0 and replay_buffer.size() > batch_size:
        print(f"🔹 Episode {episode+1}: Total Reward = {total_reward:.2f}, Moving Avg Reward = {moving_avg_reward:.2f}, Loss = {loss.item():.4f}, Epsilon = {epsilon:.3f}")

    print(f"Episode {episode+1}: Total Reward = {sum(r for _, _, r, _, _ in episode_data)}")
    print(datetime.now())

print("Training Complete!")
# Save the trained model
torch.save(dqn.state_dict(), "pacman_dqn8.pth")
print("Model saved as pacman_dqn.pth")
print(datetime.now())