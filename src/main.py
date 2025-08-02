# Author: aqeelanwar
# Created: 12 March,2020, 7:06 PM
# Email: aqeel.anwar@gatech.edu

import json
import random
from tkinter import *
import numpy as np

size_of_board = 600
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
Green_color = '#7BC043'

# RL Agent parameters
V = {}             # state string -> value (0 to 1)
epsilon = 0.1      # Exploration rate
alpha = 0.2        # Learning rate
last_states = []   # To store visited states by the RL agent during a game


class Tic_Tac_Toe():
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.play_again_button = Button(self.window, text="Play Again", font=("cmr", 20, "bold"),
                                bg="lightgray", command=self.on_play_again_click)
        self.play_again_button.place_forget()
        # Input from user in form of clicks
        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))

        self.last_states = []  # To store visited states by the RL agent during a game
        self.reward = 0

        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3)

    def play_again(self):
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(3, 3))

    def on_play_again_click(self):
        self.canvas.delete("all")
        self.play_again_button.place_forget()
        self.play_again()
        self.reset_board = False
    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)
        # logical_position = grid value on the board
        # grid_position = actual pixel values of the center of the grid
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline=symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)

    def display_gameover(self):

        if self.X_wins:
            self.X_score += 1
            text = 'Winner:\nHuman (X)'
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'Winner:\nRL Agent (O)'
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        # Display Scores title
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text='Scores')

        # Display score lines with proper vertical spacing
        start_y = 3 * size_of_board / 4
        line_spacing = 40  # pixels between lines
        total_games = self.X_score + self.O_score + self.tie_score

        self.canvas.create_text(size_of_board / 2, start_y, font="cmr 30 bold", fill=Green_color,
                                text=f'Total Games Played: {total_games}')
        self.canvas.create_text(size_of_board / 2, start_y + line_spacing, font="cmr 30 bold", fill=Green_color,
                                text=f'Human (X): {self.X_score}')
        self.canvas.create_text(size_of_board / 2, start_y + 2 * line_spacing, font="cmr 30 bold", fill=Green_color,
                                text=f'RL Agent (O): {self.O_score}')
        self.canvas.create_text(size_of_board / 2, start_y + 3 * line_spacing, font="cmr 30 bold", fill=Green_color,
                                text=f'Ties         : {self.tie_score}')
        self.reset_board = True

        # score_text = 'Click to play again \n'
        # self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
        #                         text=score_text)

        # Show "Play Again" button centered at the bottom
        self.play_again_button.place(relx=0.5, rely=0.53, anchor="center")

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / 3) * logical_position + size_of_board / 6

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True

    def is_winner(self, player):

        player = -1 if player == 'X' else 1

        # Three in a row
        for i in range(3):
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                return True
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                return True

        # Diagonals
        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
            return True

        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
            return True

        return False

    def is_tie(self):

        r, c = np.where(self.board_status == 0)
        tie = False
        if len(r) == 0:
            tie = True

        return tie

    def is_gameover(self):
        # Either someone wins or all grid occupied
        self.X_wins = self.is_winner('X')
        if not self.X_wins:
            self.O_wins = self.is_winner('O')

        if not self.O_wins:
            self.tie = self.is_tie()

        gameover = self.X_wins or self.O_wins or self.tie

        if self.X_wins:
            print('X wins')
            self.reward = 0
            self.update_state_value()
        if self.O_wins:
            print('O wins')
            self.reward = 1
            self.update_state_value()
        if self.tie:
            print('Its a tie')
            self.reward = 0
            self.update_state_value()

        return gameover


    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.reset_board:
            if self.player_X_turns:
                if not self.is_grid_occupied(logical_position):
                    self.draw_X(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = -1
                    self.player_X_turns = not self.player_X_turns
                
                logical_position = self.RL_agent_turn()
                if logical_position is not None and not self.is_grid_occupied(logical_position):
                    # Draw O only if the position is vacant
                    self.draw_O(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = 1
                    self.player_X_turns = not self.player_X_turns
            # else:
            #     if not self.is_grid_occupied(logical_position):
            #         self.draw_O(logical_position)
            #         self.board_status[logical_position[0]][logical_position[1]] = 1
            #         self.player_X_turns = not self.player_X_turns

            # Check if game is concluded
            if self.is_gameover():
                self.display_gameover()
                # print('Done')
        else:  # Play Again
            self.canvas.delete("all")
            self.last_states = []
            self.play_again()
            self.reset_board = False


    # ------------------------------------------------------------------
    # RL Agent Functions:
    # The modules required to carry out RL Agent logic
    # ------------------------------------------------------------------

    # Returns a string representation of the current board state
    def get_state_string(self):
        cell_values = ''
        for row in self.board_status:
            for cell in row:
                if cell == 1:
                    cell_values += '1'
                elif cell == -1:
                    cell_values += '-'
                else:
                    cell_values += '0'
        return cell_values
        # return ''.join(str(int(cell)) for row in self.board_status for cell in row) 

    def update_state_value(self):
        V[self.last_states[-1]] = self.reward
        new_value = 0
        old_value = 0
        next_value = 0

        for i in range(len(self.last_states) - 2, -1, -1):
            current_state = self.last_states[i]
            next_state = self.last_states[i + 1]

            old_value = V[current_state]
            next_value = V[next_state]

            new_value = old_value + alpha * (next_value - old_value)
            V[current_state] = new_value
        
        self.save_state_values()

    # RL Agent's turn to play
    def RL_agent_turn(self):
        # Get the current state as a string
        current_state = self.get_state_string()

        # Check vacant cells in the board
        vacant_cells = np.argwhere(self.board_status == 0)
        
        if len(vacant_cells) == 0:
            return None  # No vacant cells available
        
        # Convert string to state list with proper int values
        state_list = []
        for c in current_state:
            if c == '1':
                state_list.append(1)
            elif c == '-':
                state_list.append(-1)
            else:
                state_list.append(0)
            
        next_possible_move_states= []

        # Generate new states for each possible move
        for row, col in vacant_cells:
            new_state = state_list.copy()
            pos = row * 3 + col
            new_state[pos] = 1
            new_state_str = ''.join(str(x) for x in new_state)

            # Add the new state to the list of next move states
            next_possible_move_states.append([[row, col], new_state_str])

            # Update the value function if the new state is not already present
            if new_state_str not in V:
                V[new_state_str] = 0.5
        
        # Choose a random move from the next possible states
        if random.random() < epsilon:
            # Explore: choose a random move
            chosen_move = random.choice(next_possible_move_states)
        else:
            # Exploit: choose the move with the highest value
            chosen_move = max(next_possible_move_states, key=lambda x: V[x[1]])

        self.last_states.append(chosen_move[1])  # Store the state string of the chosen move
        return np.array(chosen_move[0])
    
    def save_state_values(self, filename="state_values.txt"):
        with open(filename, "w") as file:
            for state, value in V.items():
                line = f"{state}:{value}\n"
                file.write(line)

    # def save_state_values(self, filename="state_values.json"):
    #     with open(filename, "w") as f:
    #         json.dump(V, f)

# ------------------------------------------------------------------
# Main Function:
# ------------------------------------------------------------------

game_instance = Tic_Tac_Toe()
game_instance.mainloop()