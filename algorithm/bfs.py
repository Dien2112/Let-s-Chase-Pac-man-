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
def start_bfs_thread_loop(game_map, game_instance):
        ghost_pos = find_index(game_map, 'b')  # Find the ghost's current position
        pacman_pos = find_index(game_map, '2')  # Find Pac-Man's current position

        if ghost_pos and pacman_pos:
            # Call BFS to get the path and performance record
            path, record = bfs(ghost_pos, pacman_pos, game_map)

            # If path has more than 1 step (move to next step)
            if len(path) > 1:
                next_step = path[1]  # Get the next position in the path (not the current position)

                if isinstance(next_step, PerformanceRecord):
                    next_step = (next_step.x, next_step.y)  

                swap(game_map, ghost_pos, next_step)

def start_bfs_thread(game_map, game_instance):
    while game_instance.running:
        start_bfs_thread_loop(game_map, game_instance)
        time.sleep(0.6)  # Delay between moves (to simulate ghost movement)

