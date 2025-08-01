import numpy as np


def find_pos(cell):
    # Assuming cell is a 2D numpy array index
    row, col = cell
    return row * 3 + col  # Convert to a single index for a 3x3 board


board_status = np.zeros(shape=(3, 3))

board_status = np.array([
    [0, -1, 0],
    [0, 1, 1],
    [1, -1, -1]
])

current_state = ''.join(str(int(cell)) for row in board_status for cell in row) 

vacant_cells = np.argwhere(board_status == 0)

print("Current State:", current_state)
print("Vacant Cells:", vacant_cells)

current_state_list = []
i = 0

while i < len(current_state):
    if current_state[i] == '-':
        current_state_list.append(-int(current_state[i+1]))
        i += 2
    else:
        current_state_list.append(int(current_state[i]))
        i += 1

for cell in vacant_cells:
    new_state_list = current_state_list.copy()
    pos  = find_pos(cell)
    new_state_list[pos] = 1
    new_state = ''.join(str(int(x)) for x in new_state_list)
    print("New State:", new_state)