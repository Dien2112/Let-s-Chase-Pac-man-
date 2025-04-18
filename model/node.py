class Node:
    def __init__(self, position, parent=None, g=0, h=0):
        self.position = position  # [row, col]
        self.children = []        # List of child nodes (for DFS, BFS)
        self.parent = parent     # Parent node for path reconstruction
        self.g = g               # Cost from start to this node (for UCS, A*)
        self.h = h               # Heuristic estimate to goal (for A*)
        self.f = g + h           # Total estimated cost (for A*)
    
    def __eq__(self, other):
        return self.position == other.position
    
    def __lt__(self, other):
        return self.f < other.f  # For priority queue in UCS and A*