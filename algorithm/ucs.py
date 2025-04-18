# ucs.py
import heapq
import time
from utils import find_index, swap, get_neighbors
from performance import PerformanceRecord

def ucs(start, goal, game_map):
    record = PerformanceRecord()
    record.start()

    open_set = []
    heapq.heappush(open_set, (0, start))
    g_scores = {start: 0}
    came_from = {}

    while open_set:
        _, current = heapq.heappop(open_set)
        record.nodes_expanded += 1

        if current == goal:
            break

        for neighbor in get_neighbors(current, game_map):
            tentative_g_score = g_scores[current] + 1
            if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g_score
                came_from[neighbor] = current
                heapq.heappush(open_set, (g_scores[neighbor], neighbor))

    # Reconstruct path
    path = []
    if goal in came_from or start == goal:
        cur = goal
        while cur != start:
            path.append(cur)
            cur = came_from[cur]
        path.append(start)
        path.reverse()

    record.path_length = len(path)
    record.stop()
    return path, record

def start_ucs_thread(game_map, game_instance):
    while game_instance.running:
        ghost_pos = find_index(game_map, 'c')  # Find the ghost's current position
        pacman_pos = find_index(game_map, '2')  # Find Pac-Man's current position

        if ghost_pos and pacman_pos:
            # Call UCS to get the path and performance record
            path, record = ucs(ghost_pos, pacman_pos, game_map)

            # If path has more than 1 step (move to next step)
            if len(path) > 1:
                next_step = path[1]  # Get the next position in the path (not the current position)

                print(f"Ghost moved from {ghost_pos} to {next_step}")

                # Ensure next_step is a tuple (coordinates) and not a PerformanceRecord object
                if isinstance(next_step, PerformanceRecord):
                    next_step = (next_step.x, next_step.y)  # Extract coordinates from PerformanceRecord

                # Now `next_step` is guaranteed to be a tuple (row, col), and can be used with swap
                swap(game_map, ghost_pos, next_step)  # Swap the ghost's position on the map
                game_instance.check_collision()  # Check if the move caused any collision

        time.sleep(0.6)  # Delay between moves (to simulate ghost movement)

