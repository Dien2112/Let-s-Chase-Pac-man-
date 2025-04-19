# dfs.py
import time
from utils import find_index, swap, get_neighbors

def dfs_recursive(current, goal, game_map, visited, path):
    if current == goal:
        path.append(current)
        return True

    visited.add(current)
    for neighbor in get_neighbors(current, game_map):
        if neighbor not in visited:
            if dfs_recursive(neighbor, goal, game_map, visited, path):
                path.append(current)
                return True
    return False
from performance import PerformanceRecord

def dfs(start, goal, game_map):
    record = PerformanceRecord()
    record.start()

    stack = [start]
    visited = set()
    parent = {}
    
    while stack:
        current = stack.pop()
        visited.add(current)
        record.nodes_expanded += 1

        if current == goal:
            break

        for neighbor in get_neighbors(current, game_map):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    # Reconstruct path
    path = []
    if goal in parent or start == goal:
        cur = goal
        while cur != start:
            path.append(cur)
            cur = parent[cur]
        path.append(start)
        path.reverse()

    record.path_length = len(path)
    record.stop()
    return path, record

def start_dfs_thread_loop(game_map, game_instance):
    ghost_pos = find_index(game_map, 'a')  # Find the ghost's current position
    pacman_pos = find_index(game_map, '2')  # Find Pac-Man's current position
    if ghost_pos and pacman_pos:
        # Call DFS to get the path and performance record
        path, record = dfs(ghost_pos, pacman_pos, game_map)
        # If path has more than 1 step (move to next step)
        if len(path) > 1:
            next_step = path[1]  
            if isinstance(next_step, PerformanceRecord):
                next_step = (next_step.x, next_step.y)  # Extract coordinates from PerformanceRecord
            # Now `next_step` is guaranteed to be a tuple (row, col), and can be used with swap
            swap(game_map, ghost_pos, next_step)  # Swap the ghost's position on the map
            
            game_instance.check_collision()  # Check if the move caused any collision
def start_dfs_thread(game_map, game_instance):
    while game_instance.running:
        print("Moved")
        start_dfs_thread_loop(game_map, game_instance)
        print("Moving")
        time.sleep(0.6)  # Delay between moves (to simulate ghost movement)
