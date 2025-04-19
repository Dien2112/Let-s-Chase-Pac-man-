def find_index(matrix, target):
    for i, row in enumerate(matrix):
        if target in row:
            return (i, row.index(target))
    return None

def valid_way(matrix, index):
    result = []
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = index[0]+dx, index[1]+dy
        if 0 <= nx < len(matrix) and 0 <= ny < len(matrix[0]) and matrix[nx][ny] != '0':
            result.append((nx, ny))
    return result


def swap(table, cell1, cell2):
    # Ensure the positions are tuples like (row, col)
    if isinstance(cell1, tuple) and isinstance(cell2, tuple):
        table[cell1[0]][cell1[1]], table[cell2[0]][cell2[1]] = table[cell2[0]][cell2[1]], table[cell1[0]][cell1[1]]
    else:
        print("Error: Positions must be tuples or lists")
def get_neighbors(pos, game_map):
    """
    Returns valid neighbor positions (row, col) around the current position.
    Only considers positions that are within bounds and not walls ('0').
    """
    neighbors = []
    row, col = pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < len(game_map) and 0 <= c < len(game_map[0]):
            if game_map[r][c] == '1' or game_map[r][c] == '2':  # Not a wall
                neighbors.append((r, c))
    
    return neighbors
def complex_map_to_map(map):
    converted_map = []
    for row in map:
        new_row = []
        for cell in row:
            if cell == 'X' or (cell >='0' and cell <='9'):  # Wall-like characters
                new_row.append('0')
            elif cell == 'e':
                new_row.append('2')
            elif cell in ['a', 'b', 'c', 'd']:  # Ghosts
                new_row.append(cell)
            else:
                new_row.append('1')  # fallback: assume walkable
        converted_map.append(new_row)
    return converted_map
