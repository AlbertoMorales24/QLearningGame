import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

# Define the DQN Model
class DQN(nn.Module):
    def __init__(self, input_channels=4, action_size=4):
        super(DQN, self).__init__()

        # Convolutional layers to process the state input
        self.conv1 = nn.Conv2d(input_channels, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)

        # Fully connected layers to output Q-values for actions
        self.fc1 = nn.Linear(128 * 7 * 7, 512)  # Flatten 7x7 conv output
        self.fc2 = nn.Linear(512, action_size)  # Output Q-values for each action

    def forward(self, state):
        x = F.relu(self.conv1(state))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))

        x = x.view(x.size(0), -1)  # Flatten
        x = F.relu(self.fc1(x))
        x = self.fc2(x)  # No activation for raw Q-values
        return x
