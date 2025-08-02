# Tic-Tac-Toe with Reinforcement Learning Agent (TD(0) Evaluation)

## 📚 Description

This project is an interactive Tic-Tac-Toe game with a reinforcement learning (RL) agent trained using **temporal-difference learning (TD(0))**, as introduced in the book:

> **"Reinforcement Learning: An Introduction"**  
> by **Richard S. Sutton** and **Andrew G. Barto**  
> [Link to book](http://incompleteideas.net/book/the-book-2nd.html)

The RL agent learns **state values** through repeated play using TD updates and an **ε-greedy** strategy to balance **exploration** and **exploitation**.

## 🧠 Core Concepts Implemented

- **State Representation**: The board is represented as a string (e.g., `'1-100111-1-1'`) for easy lookup and tracking in the value function dictionary.
- **Tabular Value Function (V)**: The agent estimates how good a state is (in terms of winning chances) by assigning a value between 0 and 1.
- **Temporal-Difference Learning (TD(0))**: After each game, the agent updates its state value estimates using the TD(0) rule:

$$
V(s_t) \leftarrow V(s_t) + \alpha [V(s_{t+1}) - V(s_t)]
$$

- **ε-greedy Action Selection**: With probability ε (e.g., 0.1), the agent explores a random action; otherwise, it exploits the best-known action.

## 👨‍💻 Credit

- Original GUI and game logic for human vs human Tic-Tac-Toe was developed by:
> **Author:** Aqeel Anwar  
> **Created:** 12 March 2020  
> **Email:** aqeel.anwar@gatech.edu  
> [GitHub Profile](https://github.com/aqeelanwar)

## 🛠️ What I Implemented

- Integrated an RL agent (Player O) to play against a human (Player X).
- Developed state encoding logic for board positions.
- Implemented value function learning using the TD(0) algorithm.
- Added exploration via ε-greedy move selection.
- Tracked and stored game history (`last_states`) for backpropagating rewards.
- Wrote logic to save state values to a `.txt` file for future reference.

## 📁 Saved Output

- Trained value function is saved to `state_values.txt` after each game.
- Each line is in the format:  

For example:
`1-100111-1-1:0.732`
`0-110111-1-1:0.481`


## 🔮 Future Improvements

- Load and resume learning from saved `state_values.txt`.
- Add **epsilon decay** to reduce exploration over time.
- Train the agent via self-play (instead of requiring a human opponent).
- Use a Q-learning approach with action-value pairs (Q(s, a)) instead of only V(s).
- Visualize learning progress over time (e.g., win rate graph).
- Port the game to a web app using Flask or Streamlit.

## 🚀 How to Run

Make sure you have Python 3 and `numpy` installed.

```bash
python main.py
```

Then click on the board to play against the agent!


Let me know if you'd like it saved as a `README.md` file or included in your project folder automatically.
