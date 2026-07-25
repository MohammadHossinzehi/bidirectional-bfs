from collections import deque
from typing import Dict, List, Tuple, Optional, Set
import heapq


class Graph:
    """Undirected graph representation with bidirectional BFS pathfinding."""
    
    def __init__(self):
        self.adjacency: Dict[str, List[str]] = {}
    
    def add_edge(self, u: str, v: str, weight: int = 1) -> None:
        """Add an undirected edge between nodes u and v."""
        if u not in self.adjacency:
            self.adjacency[u] = []
        if v not in self.adjacency:
            self.adjacency[v] = []
        
        self.adjacency[u].append(v)
        self.adjacency[v].append(u)
    
    def add_node(self, node: str) -> None:
        """Add an isolated node."""
        if node not in self.adjacency:
            self.adjacency[node] = []
    
    def get_neighbors(self, node: str) -> List[str]:
        """Return neighbors of a node."""
        return self.adjacency.get(node, [])
    
    def has_node(self, node: str) -> bool:
        """Check if a node exists."""
        return node in self.adjacency
    
    def num_nodes(self) -> int:
        """Return number of nodes."""
        return len(self.adjacency)
    
    def num_edges(self) -> int:
        """Return number of edges."""
        return sum(len(neighbors) for neighbors in self.adjacency.values()) // 2


class BidirectionalBFS:
    """Bidirectional BFS shortest path finder."""
    
    def __init__(self, graph: Graph):
        self.graph = graph
        self.forward_parent: Dict[str, Optional[str]] = {}
        self.backward_parent: Dict[str, Optional[str]] = {}
        self.forward_distance: Dict[str, int] = {}
        self.backward_distance: Dict[str, int] = {}
        self.meeting_point: Optional[str] = None
        self.exploration_stats = {"forward_explored": 0, "backward_explored": 0}
    
    def find_shortest_path(self, source: str, target: str) -> Optional[List[str]]:
        """
        Find shortest path from source to target using bidirectional BFS.
        Returns the path as a list of nodes, or None if no path exists.
        """
        if not self.graph.has_node(source) or not self.graph.has_node(target):
            return None
        
        if source == target:
            return [source]
        
        # Reset state
        self.forward_parent = {source: None}
        self.backward_parent = {target: None}
        self.forward_distance = {source: 0}
        self.backward_distance = {target: 0}
        self.meeting_point = None
        self.exploration_stats = {"forward_explored": 0, "backward_explored": 0}
        
        forward_queue = deque([source])
        backward_queue = deque([target])
        
        while forward_queue or backward_queue:
            # Expand forward frontier
            if forward_queue:
                if self._expand_frontier(
                    forward_queue, self.forward_parent, self.backward_parent,
                    self.forward_distance, self.backward_distance, "forward"
                ):
                    return self._reconstruct_path()
            
            # Expand backward frontier
            if backward_queue:
                if self._expand_frontier(
                    backward_queue, self.backward_parent, self.forward_parent,
                    self.backward_distance, self.forward_distance, "backward"
                ):
                    return self._reconstruct_path()
        
        return None
    
    def _expand_frontier(
        self,
        queue: deque,
        parent_map: Dict[str, Optional[str]],
        other_parent_map: Dict[str, Optional[str]],
        distance_map: Dict[str, int],
        other_distance_map: Dict[str, int],
        direction: str
    ) -> bool:
        """Expand frontier in one direction. Return True if meeting point found."""
        if not queue:
            return False
        
        current = queue.popleft()
        current_dist = distance_map[current]
        
        if direction == "forward":
            self.exploration_stats["forward_explored"] += 1
        else:
            self.exploration_stats["backward_explored"] += 1
        
        for neighbor in self.graph.get_neighbors(current):
            if neighbor not in parent_map:
                parent_map[neighbor] = current
                distance_map[neighbor] = current_dist + 1
                queue.append(neighbor)
                
                # Check if we met the other search
                if neighbor in other_parent_map:
                    self.meeting_point = neighbor
                    return True
        
        return False
    
    def _reconstruct_path(self) -> List[str]:
        """Reconstruct path from source to target via meeting point."""
        if self.meeting_point is None:
            return []
        
        # Build path from source to meeting point
        path_forward = []
        current = self.meeting_point
        while current is not None:
            path_forward.append(current)
            current = self.forward_parent.get(current)
        path_forward.reverse()
        
        # Build path from meeting point to target
        path_backward = []
        current = self.backward_parent.get(self.meeting_point)
        while current is not None:
            path_backward.append(current)
            current = self.backward_parent.get(current)
        
        return path_forward + path_backward
    
    def get_exploration_stats(self) -> Dict[str, int]:
        """Return statistics about the search."""
        return self.exploration_stats.copy()


def create_sample_graph() -> Graph:
    """Create a sample graph for testing."""
    graph = Graph()
    edges = [
        ("A", "B"), ("A", "C"), ("B", "D"),
        ("C", "E"), ("D", "E"), ("D", "F"),
        ("E", "G"), ("F", "G"), ("G", "H")
    ]
    
    for u, v in edges:
        graph.add_edge(u, v)
    
    return graph


if __name__ == "__main__":
    # Example usage
    graph = create_sample_graph()
    print(f"Graph created with {graph.num_nodes()} nodes and {graph.num_edges()} edges.")
    
    finder = BidirectionalBFS(graph)
    path = finder.find_shortest_path("A", "H")
    
    if path:
        print(f"Shortest path from A to H: {' -> '.join(path)}")
        print(f"Path length: {len(path) - 1} edges")
        stats = finder.get_exploration_stats()
        print(f"Exploration stats: Forward={stats['forward_explored']}, Backward={stats['backward_explored']}")
    else:
        print("No path found from A to H")
