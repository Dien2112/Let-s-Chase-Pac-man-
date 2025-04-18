# performance.py
import time
import tracemalloc

class PerformanceRecord:
    def __init__(self):
        self.execution_time = 0
        self.memory_usage = 0
        self.nodes_expanded = 0
        self.path_length = 0

    def start(self):
        tracemalloc.start()
        self._start_time = time.time()

    def stop(self):
        self.execution_time = time.time() - self._start_time
        current, peak = tracemalloc.get_traced_memory()
        self.memory_usage = peak
        tracemalloc.stop()

    def reset(self):
        self.execution_time = 0
        self.memory_usage = 0
        self.nodes_expanded = 0
        self.path_length = 0

    def as_dict(self):
        return {
            "Time": f"{self.execution_time:.4f}s",
            "Memory": f"{self.memory_usage / 1024:.2f} KB",
            "Expanded": self.nodes_expanded,
            "Path": self.path_length
        }
