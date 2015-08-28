import unittest
from structure.config import *


class MyTestCase(unittest.TestCase):

    def test_str(self):
        vertices = ['A', 'B', 'C', 'D']
        edges = [['D', 'B'], ['A', 'D']]
        weights = [7, 3]
        graph = DiGraph(vertices, edges, weights)
        self.assertEqual(str(graph),"[[A, ['D']], [B, []], [C, []], [D, ['B']]]")
        self.assertEqual(str(graph.V), "[A, B, C, D]")
        self.assertEqual(str(graph.E), "[['D', 'B'], ['A', 'D']]")
        self.assertEqual(len(graph), 4)

        #test getEdge
        # self.assertEqual(str(graph.getEdge('D', 'A')), "['A', 'D']")
        self.assertEqual(str(graph.getEdge('A', 'D')), "['A', 'D']")

        #test getEdgesOfNode
        self.assertEqual(str(graph.getEdgesOfNode('D')), "[['D', 'B']]")

        #test adjacent vertices
        self.assertEqual(str(graph.getAdjVertices('D')), "[B]")

        #test get weight
        self.assertEqual(graph.getWeight('D', 'B'), 7)

        #test addEdge
        graph.addEdge(['A', 'B'])
        self.assertEqual(str(graph.E), "[['D', 'B'], ['A', 'D'], ['A', 'B']]")

        #test delEdge
        graph.delEdge(['A', 'B'])
        self.assertEqual(str(graph.E), "[['D', 'B'], ['A', 'D']]")

        #test addVertex
        graph.addVertex('E')
        self.assertEqual(str(graph.V), "[A, B, C, D, E]")

        #test delVertex
        graph.delVertex('D')
        self.assertEqual(str(graph.V), "[A, B, C, E]")
        self.assertEqual(str(graph.E), "[]")

        #test random
        graph = DiGraph.random()
        print(graph)


if __name__ == '__main__':
    unittest.main()
