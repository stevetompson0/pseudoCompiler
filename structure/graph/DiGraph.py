'''
Author: Fang Zhou
Date: 2015/6/17
Version: 1.0
Description:
Directional Graph data structure, extend Graph
'''

from structure.config import *
import glb

class DiGraph(Graph):
    __name__ =  "DiGraph"


    '''
    Overwrite Graph functions:
    addEdge(self, edge, weight)
    delEdge(self, edge)
    getEdge(self, from_node, to_node)

    random(cls)
    '''

    def addEdge(self, edge, weight=1):
        assert(len(edge) == 2)
        vex1, vex2 = edge

        if self.checkEdge(edge):
            raise KeyError('edge {} already exist in this graph'.format(edge))

        self.getVertex(vex1).addAdjVertex(vex2)
        self._edges.append(Edge(edge,weight))

    def delEdge(self, edge):
        assert(len(edge) == 2)

        vex1, vex2 = edge
        if not self.checkEdge(edge):
            raise KeyError('edge {} cannot be found'.format(edge))

        self.getVertex(vex1).delAdjVertex(vex2)
        self._edges.pop(self._edges.index(edge))

    def getEdge(self, from_node, to_node):
        if isinstance(from_node, Vertex):
            from_node = from_node.value
        if isinstance(to_node, Vertex):
            to_node = to_node.value
        return self._edges[self._edges.index(Edge([from_node, to_node]))]

    #get all edges start from from_node
    def getEdgesOfNode(self, from_node):
        if isinstance(from_node, Vertex):
            from_node = from_node._value

        edgeList = []
        for x in self.E:
            if from_node is x.vertex_pair[0]:
                edgeList.append(x)
        return edgeList

    #generate a graph randomly
    @classmethod
    def random(cls):
        import random, math, string

        vexNo = random.randint(glb.randomLowRange, glb.randomUpperRange)
        edgeNo = random.randint(vexNo-1, math.floor(vexNo*(vexNo-1)/2))

        vertexNameList = random.sample(string.ascii_uppercase, vexNo)
        edgePairList = []
        weightList = []

        #To make sure every vertex is connected
        for i in range(0, vexNo-1):
            edgePairList.append([vertexNameList[i], vertexNameList[i+1]])

        for i in range(0, edgeNo - vexNo + 1):
            node1 = random.choice(vertexNameList)
            node2 = random.choice(vertexNameList)
            tempEdge = [node1, node2]

            #select another nodes if edge already exists or node1 equals to node2
            while tempEdge in edgePairList or node1 == node2:
                node1 = random.choice(vertexNameList)
                node2 = random.choice(vertexNameList)
                tempEdge = [node1, node2]

            edgePairList.append(tempEdge)


        for i in range(0, edgeNo):
            weightList.append(random.randint(1,15))

        return DiGraph(vertexNameList, edgePairList, weightList)


