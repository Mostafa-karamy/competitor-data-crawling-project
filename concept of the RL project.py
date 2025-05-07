import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns

# Define states (discrete buckets)
price_levels = [0, 1, 2]  # 0 = low, 1 = medium, 2 = high
competitor_levels = [0, 1, 2]
market_conditions = [0, 1, 2]
inventory_levels = [0, 1, 2]

# Number of discrete states
num_states = len(price_levels) * len(competitor_levels) * len(market_conditions) * len(inventory_levels)

# Define actions
actions = [0, 1, 2]  # 0 = lower price, 1 = keep price, 2 = raise price
num_actions = len(actions)

# Initialize Q-table
Q = np.zeros((num_states, num_actions))

# Hyperparameters
alpha = 0.1       # learning rate
gamma = 0.9       # discount factor
epsilon = 0.2     # exploration rate
epsilon_decay = 0.995
min_epsilon = 0.1
num_episodes = 1000

# Helper: map multi-dimensional state to a single index
def state_to_index(price, c1, market, inventory):
    return (price * 27 + c1 * 9 + market * 3 + inventory)

# Reward function (improved)
def get_reward(price, c1, market, inventory):
    base_demand = 10 + (market * 5)
    
    # Price sensitivity: the effect of competitor price on demand
    price_diff = price - c1
    if price_diff < 0:  # lower than competitor
        units_sold = base_demand + 5 + (abs(price_diff) * 2)  # Scaling demand
    elif price_diff == 0:  # same as competitor
        units_sold = base_demand
    else:  # higher than competitor
        units_sold = max(base_demand - (price_diff * 2), 0)  # Penalty for higher price
    
    # Incorporating inventory level into the reward
    inventory_factor = 1 + (inventory - 1) * 0.2  # for inventory levels 0, 1, and 2
    units_sold *= inventory_factor
    
    profit = price * units_sold
    return profit

# Main loop
reward_history = []
for episode in range(num_episodes):
    # Random initial state
    price = random.choice(price_levels)
    c1 = random.choice(competitor_levels)
    market = random.choice(market_conditions)
    inventory = random.choice(inventory_levels)
    state = state_to_index(price, c1, market, inventory)

    total_reward = 0

    for step in range(100):  # steps per episode
        # Epsilon-greedy action
        if random.uniform(0, 1) < epsilon:
            action = random.choice(actions)
        else:
            action = np.argmax(Q[state, :])

        # Apply action: adjust price
        if action == 0 and price > 0:  # Lower price
            price = max(0, price - random.choice([1, 2]))  # Allow larger decreases
        elif action == 2 and price < 2:  # Raise price
            price = min(2, price + random.choice([1, 2]))  # Allow larger increases

        # Randomly update competitor and market (for simplicity)
        c1 = random.choice(competitor_levels)
        market = random.choice(market_conditions)
        inventory = random.choice(inventory_levels)

        next_state = state_to_index(price, c1, market, inventory)
        reward = get_reward(price, c1, market, inventory)
        total_reward += reward

        # Q-learning update
        Q[state, action] = (1 - alpha) * Q[state, action] + alpha * (reward + gamma * np.max(Q[next_state, :]))

        state = next_state

    reward_history.append(total_reward)

    # Decay epsilon (exploration rate)
    epsilon = max(min_epsilon, epsilon * epsilon_decay)

# After training, print learned Q-values
print("Learned Q-table:")
print(Q)

# Plotting Q-values for specific states
q_values = np.random.rand(6, 3)  # Example for illustration, replace with actual Q-values

selected_states = [0, 2, 5]  # pick example states
for state in selected_states:
    plt.figure()
    plt.bar(range(q_values.shape[1]), q_values[state])
    plt.xlabel('Actions')
    plt.ylabel('Q-value')
    plt.title(f'Q-values for State {state}')
    plt.xticks(range(q_values.shape[1]), [f'Action {i}' for i in range(q_values.shape[1])])
    plt.show()

# Example of cumulative reward across episodes
plt.figure()
plt.plot(range(num_episodes), reward_history)
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.title('Learning Curve: Reward over Episodes')
plt.show()
