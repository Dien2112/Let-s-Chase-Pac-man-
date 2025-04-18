import time
from utils import find_index, swap, get_neighbors
from collections import deque
from performance import PerformanceRecord

def bfs(start, goal, game_map):
    record = PerformanceRecord()
    record.start()

    queue = deque([start])
    visited = set([start])
    parent = {}

    while queue:
        current = queue.popleft()
        record.nodes_expanded += 1

        if current == goal:
            break

        for neighbor in get_neighbors(current, game_map):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

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

def start_bfs_thread(game_map, game_instance):
    while game_instance.running:
        ghost_pos = find_index(game_map, 'b')  # Find the ghost's current position
        pacman_pos = find_index(game_map, '2')  # Find Pac-Man's current position

        if ghost_pos and pacman_pos:
            # Call BFS to get the path and performance record
            path, record = bfs(ghost_pos, pacman_pos, game_map)
            print(f"Path found: {path}")
            

            # If path has more than 1 step (move to next step)
            if len(path) > 1:
                next_step = path[1]  # Get the next position in the path (not the current position)

                print(f"Ghost moved from {ghost_pos} to {next_step}")
                if isinstance(next_step, PerformanceRecord):
                    next_step = (next_step.x, next_step.y)  # Extract coordinates from PerformanceRecord

                print(f"Before swap, ghost at {ghost_pos}: {game_map[ghost_pos[0]][ghost_pos[1]]}")
                print(f"Before swap, next step at {next_step}: {game_map[next_step[0]][next_step[1]]}")

                swap(game_map, ghost_pos, next_step)

                print(f"After swap, ghost at {ghost_pos}: {game_map[ghost_pos[0]][ghost_pos[1]]}")
                print(f"After swap, next step at {next_step}: {game_map[next_step[0]][next_step[1]]}")
                game_instance.check_collision()  # Check for collision after moving

        time.sleep(0.6)  # Delay between moves (to simulate ghost movement)

