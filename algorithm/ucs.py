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
    parent = {}

    while open_set:
        _, current = heapq.heappop(open_set)
        record.nodes_expanded += 1

        if current == goal:
            break

        for neighbor in get_neighbors(current, game_map):
            tentative_g_score = g_scores[current] + 1
            if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g_score
                parent[neighbor] = current
                heapq.heappush(open_set, (g_scores[neighbor], neighbor))

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

def start_ucs_thread_loop(game_map, game_instance):

    ghost_pos = find_index(game_map, 'c')  
    pacman_pos = find_index(game_map, '2') 
    
    if ghost_pos and pacman_pos:
        path, record = ucs(ghost_pos, pacman_pos, game_map)
        if len(path) > 1:
            next_step = path[1]  
            if isinstance(next_step, PerformanceRecord):
                next_step = (next_step.x, next_step.y)  
            swap(game_map, ghost_pos, next_step)  
            game_instance.check_collision() 

def start_ucs_thread(game_map, game_instance):
    while game_instance.running:
        start_ucs_thread_loop(game_map, game_instance)
        time.sleep(0.6) 

