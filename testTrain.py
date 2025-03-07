import torch
import numpy as np
from gameTraining import game
from DQN import DQN

# Load trained model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
dqn = DQN().to(device)
dqn.load_state_dict(torch.load("pacman_dqn8.pth", map_location=device))
dqn.eval()  # Set to evaluation mode

def get_action(state):
    """Chooses an action using epsilon-greedy strategy."""
    global epsilon

    # Check if state is already a tensor
    if isinstance(state, np.ndarray):  # Convert only if it's a NumPy array
        state_tensor = torch.from_numpy(state).float().permute(2, 0, 1).unsqueeze(0).to(device)  # (1, 4, 10, 10)
    elif isinstance(state, torch.Tensor):  # If already a tensor, ensure correct shape
        if state.dim() == 3:  # (4, 7, 7) → Needs batch dimension
            state_tensor = state.unsqueeze(0).to(device)  # (1, 4, 7, 7)
        elif state.dim() == 4:  # (1, 4, 7, 7) → Already correct
            state_tensor = state.to(device)
        else:
            raise ValueError(f"Unexpected state shape: {state.shape}")  # Debugging

    with torch.no_grad():
        q_values = dqn(state_tensor)  # Expecting (1, 4, 7, 7)
        return torch.argmax(q_values).item()  # Best action