import unittest
from structure.config import *


class MyTestCase(unittest.TestCase):

    def test_vertex(self):
        a = Vertex('A')
        b = Vertex('B')
        c = Vertex('C', [b])

        #test add vertex
        c.addAdjVertex(a)

        #test adjacent vertices
        self.assertEqual(str(c.adjVertices), '[B, A]')

        #test __str__
        self.assertEqual(str(c), 'C')

        #test __iter__
        for ele in c:
            print(ele)

        #test getitem
        self.assertEqual(str(c[1]), 'A')

        #test delete vertex
        # c.delAdjVertex(c)
        c.delAdjVertex(b)

    def test_edge(self):
        e1 = Edge(('A', 'B'), 2)
        self.assertEqual(str(e1), "('A', 'B')")
        self.assertEqual(str(e1.start), 'A')
        self.assertEqual(str(e1.end), 'B')
        self.assertEqual(e1.weight, 2)



    def test_str(self):
        vertices = ['A', 'B', 'C', 'D']
        edges = [['D', 'B'], ['A', 'D']]
        weights = [7, 3]
        graph = Graph(vertices, edges, weights)
        self.assertEqual(str(graph),"[[A, ['D']], [B, ['D']], [C, []], [D, ['B', 'A']]]")
        self.assertEqual(str(graph.V), "[A, B, C, D]")
        self.assertEqual(str(graph.E), "[['D', 'B'], ['A', 'D']]")
        self.assertEqual(len(graph), 4)

        #test getEdge
        self.assertEqual(str(graph.getEdge('D', 'A')), "['A', 'D']")
        self.assertEqual(str(graph.getEdge('A', 'D')), "['A', 'D']")

        #test getEdgesOfNode
        self.assertEqual(str(graph.getEdgesOfNode('D')), "[['D', 'B'], ['A', 'D']]")

        #test adjacent vertices
        self.assertEqual(str(graph.getAdjVertices('D')), "[B, A]")

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
        graph = Graph.random()
        print(graph)


if __name__ == '__main__':
    unittest.main()
