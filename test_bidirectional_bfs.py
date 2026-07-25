import unittest
from bidirectional_bfs import Graph, BidirectionalBFS


class TestGraph(unittest.TestCase):
    """Test cases for Graph class."""
    
    def setUp(self):
        self.graph = Graph()
    
    def test_add_node(self):
        self.graph.add_node("A")
        self.assertTrue(self.graph.has_node("A"))
    
    def test_add_edge(self):
        self.graph.add_edge("A", "B")
        self.assertIn("B", self.graph.get_neighbors("A"))
        self.assertIn("A", self.graph.get_neighbors("B"))
    
    def test_undirected_edge(self):
        """Verify edges are bidirectional."""
        self.graph.add_edge("X", "Y")
        neighbors_x = self.graph.get_neighbors("X")
        neighbors_y = self.graph.get_neighbors("Y")
        self.assertIn("Y", neighbors_x)
        self.assertIn("X", neighbors_y)
    
    def test_graph_stats(self):
        self.graph.add_edge("A", "B")
        self.graph.add_edge("B", "C")
        self.assertEqual(self.graph.num_nodes(), 3)
        self.assertEqual(self.graph.num_edges(), 2)
    
    def test_isolated_node(self):
        self.graph.add_node("lonely")
        self.assertEqual(len(self.graph.get_neighbors("lonely")), 0)


class TestBidirectionalBFS(unittest.TestCase):
    """Test cases for BidirectionalBFS pathfinder."""
    
    def setUp(self):
        self.graph = Graph()
        # Create a simple chain graph: A-B-C-D-E
        edges = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")]
        for u, v in edges:
            self.graph.add_edge(u, v)
        self.finder = BidirectionalBFS(self.graph)
    
    def test_path_exists(self):
        """Test finding path in connected graph."""
        path = self.finder.find_shortest_path("A", "E")
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 5)
        self.assertEqual(path[0], "A")
        self.assertEqual(path[-1], "E")
    
    def test_same_node(self):
        """Test path from node to itself."""
        path = self.finder.find_shortest_path("C", "C")
        self.assertEqual(path, ["C"])
    
    def test_adjacent_nodes(self):
        """Test path between adjacent nodes."""
        path = self.finder.find_shortest_path("A", "B")
        self.assertEqual(path, ["A", "B"])
    
    def test_shortest_path_correctness(self):
        """Test that shortest path is indeed minimal."""
        graph = Graph()
        # Create a diamond graph: A connects to B and C, both connect to D
        edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]
        for u, v in edges:
            graph.add_edge(u, v)
        
        finder = BidirectionalBFS(graph)
        path = finder.find_shortest_path("A", "D")
        self.assertEqual(len(path), 3)  # A -> B -> D or A -> C -> D
    
    def test_no_path_disconnected(self):
        """Test when no path exists."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("C", "D")  # Disconnected component
        
        finder = BidirectionalBFS(graph)
        path = finder.find_shortest_path("A", "C")
        self.assertIsNone(path)
    
    def test_nonexistent_node(self):
        """Test with non-existent source or target."""
        path = self.finder.find_shortest_path("A", "NonExistent")
        self.assertIsNone(path)
        
        path = self.finder.find_shortest_path("NonExistent", "A")
        self.assertIsNone(path)
    
    def test_exploration_stats(self):
        """Test that exploration stats are tracked."""
        path = self.finder.find_shortest_path("A", "E")
        stats = self.finder.get_exploration_stats()
        
        self.assertIn("forward_explored", stats)
        self.assertIn("backward_explored", stats)
        self.assertGreater(stats["forward_explored"] + stats["backward_explored"], 0)
    
    def test_complex_graph(self):
        """Test with a more complex graph."""
        graph = Graph()
        edges = [
            ("A", "B"), ("A", "C"), ("B", "D"),
            ("C", "E"), ("D", "E"), ("D", "F"),
            ("E", "G"), ("F", "G"), ("G", "H")
        ]
        for u, v in edges:
            graph.add_edge(u, v)
        
        finder = BidirectionalBFS(graph)
        path = finder.find_shortest_path("A", "H")
        
        self.assertIsNotNone(path)
        self.assertEqual(path[0], "A")
        self.assertEqual(path[-1], "H")
        # Verify path is continuous
        for i in range(len(path) - 1):
            self.assertIn(path[i+1], graph.get_neighbors(path[i]))


if __name__ == "__main__":
    unittest.main()
