'''
Author: Fang Zhou
Date: 2015/6/13
Version: 1.0
Description:
Graph data structure
'''

import sys
import glb

class Vertex():
    '''
    Vertex of the graph
    '''

    __name__ = 'Vertex'

    #initialize a vertex with adjacent vertices
    def __init__(self, value, adjs=[]):
        self._value = value
        self._adjVertices = adjs
        self._color = glb.DEFAULT_VERTEX_COLOR
        self._nodeFlag = glb.flag_dict['unchanged']

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._nodeFlag = glb.flag_dict['changed']
        self._value = value

    @property
    def adjVertices(self):
        return self._adjVertices

    @adjVertices.setter
    def adjVertices(self, adjs):
        self._adjVertices = adjs

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def nodeFlag(self):
        return self._nodeFlag

    @nodeFlag.setter
    def nodeFlag(self,nodeFlag):
        self._nodeFlag = nodeFlag

    def __eq__(self, obj):
        if isinstance(obj, Vertex):
            return self.value == obj.value
        else:
            return self.value == obj

    def __cmp__(self, obj):
        if isinstance(obj, Vertex):
            return __cmp__(self.value, obj.value)
        else:
            return __cmp__(self.value, obj)

    def __lt__(self, obj):
        if isinstance(obj, Vertex):
            return self.value < obj.value
        else:
            return self.value < obj

    def __gt__(self, obj):
        if isinstance(obj, Vertex):
            return self.value > obj.value
        else:
            return self.value > obj

    def __str__(self):
        return self._value

    #otherwise, it will print <objxxx> instead of str
    __repr__ = __str__

    def __len__(self):
        return len(self._adjVertices)


    def __iter__(self):
        for adj in self._adjVertices:
            yield adj


    #Change vertex color to VISITED_COLOR after visiting
    def __getitem__(self, ind):
        self._adjVertices[ind].color = glb.VISITED_COLOR
        return self._adjVertices[ind]

    def __hash__(self):
        return hash(self._value)
    
    #Add new adjacent Vertex
    def addAdjVertex(self, vex):
        # self.adjVertices = [1]
        if vex not in self._adjVertices:
            self._adjVertices.append(vex)
            self._nodeFlag = glb.flag_dict['changed']
        else:
            raise KeyError('Vertex {} already exist in {} \'s adjacent vertices list'.format(vex, self))

    #Remove one vertex from the adjacent vertices list
    def delAdjVertex(self, vex):
        if vex in self._adjVertices:
            index = self._adjVertices.index(vex)
            self._adjVertices.pop(index)
            self._nodeFlag = glb.flag_dict['changed']
        else:
            raise KeyError('Vertex {} already exist in {} \'s adjacent vertices list'.format(vex, self))


class Edge():
    '''
    Edge of graph
    '''

    __name__ = 'Edge'

    def __init__(self, pair, weight=None):
        assert(len(pair) == 2)
        self._pair = pair
        self._weight = weight or 1
        self._color = glb.DEFAULT_EDGE_COLOR

    def __str__(self):
        return str(self._pair)

    __repr__ = __str__

    def __cmp__(self, obj):
        return __cmp__(self._pair, obj._pair)

    def __eq__(self, obj):
        if isinstance(obj, Edge):
            return self._pair == obj._pair
        else:
            return self._pair[0] == obj[0] and self._pair[1] == obj[1]

    def __hash__(self):
        return hash(self._pair)


    @property
    def start(self):
        return self._pair[0]


    @property
    def end(self):
        return self._pair[1]


    @property
    def vertex_pair(self):
        return self._pair


    @property
    def weight(self):
        return self._weight

    @property
    def color(self):
        return self._color


    @weight.setter
    def weight(self, weight):
        self._weight = weight

    @color.setter
    def color(self, color):
        self._color = color


class Graph():

    __name__ = 'Graph'

    #initilize a graph, vertices: string array, edges: string pair array, weights: number array
    def __init__(self, vertices=[], edges=[], weights=[]):
        from itertools import zip_longest

        # weights should not longer than edges
        if len(weights) > len(edges):
            weights = weights[:len(edges)]

        #Attention: must use Vertex(value, []), otherwise all vertices will share the same adjVertices list
        self._vertices = [Vertex(value, []) for value in vertices]
        self._edges = []

        for edge, weight in zip_longest(edges, weights, fillvalue=1):
            self.addEdge(edge, weight)


    def __delattr__(self, name):
        self._vertices.__delattr__(name)


    def __eq__(self, obj):
        if isinstance(obj, Graph):
            return self._vertices == obj._vertices and self._edges == obj._edges
        else:
            return False


    def __str__(self):
        ret = '['
        for i in range(len(self.vertices)):
            ret += '[' + str(self.vertices[i]) + ', ' + str(self.vertices[i].adjVertices) + ']'
            if i != len(self.vertices) - 1:
                ret += ', '
        ret += ']'
        return ret

    def __hash__(self):
        return hash(self._vertices)


    def __len__(self):
        return len(self._vertices)


    def __sizeof__(self):
        return self._vertices.__sizeof__()

    @property
    def vertex_count(self):
        return len(self.V)

    @property
    def edge_count(self):
        return len(self.E)


    @property
    def V(self):
        return self._vertices

    @property
    def vertices(self):
        return self._vertices

    @property
    def E(self):
        return self._edges

    @property
    def edges(self):
        return self._edges

    #get vertex based on the name
    def getVertex(self, vex):
        return self._vertices[self._vertices.index(vex)]

    #get edge by from node and end node
    def getEdge(self, from_node, to_node):
        if isinstance(from_node, Vertex):
            from_node = from_node._value
        if isinstance(to_node, Vertex):
            to_node = to_node._value
        if Edge((from_node, to_node)) in self._edges:
            return self._edges[self._edges.index(Edge((from_node, to_node)))]
        elif Edge((to_node, from_node)) in self._edges:
            return self._edges[self._edges.index(Edge((to_node, from_node)))]
        else:
            return None

    #get all edges start from from_node
    def getEdgesOfNode(self, from_node):
        if isinstance(from_node, Vertex):
            from_node = from_node._value

        edgeList = []
        for x in self.E:
            if from_node in x.vertex_pair:
                edgeList.append(x)
        return edgeList

        # from itertools import filterfalse
        # return list(filterfalse(lambda x: from_node in x._pair, self._edges))

    def getAdjVertices(self, vex):
        return list(map(self.getVertex, self.getVertex(vex).adjVertices))

    def getWeight(self, from_node, to_node):
        edge = self.getEdge(from_node, to_node)
        if edge:
            return edge.weight
        else:
            return None

    def setWeight(self, edge, weight):
        if edge in self._edges:
            self._edges[self._edges.index(edge)].weight = weight

    #check whether vex exist in graph
    def checkVex(self, vertex):
        return (vertex in self._vertices)

    def checkEdge(self, edge):
        assert(len(edge) == 2)
        vex1, vex2 = edge

        if not ((self.checkVex(vex1)) and (self.checkVex(vex2))):
            raise NameError('edge illegal, vertex cannot be found')

        return (vex2 in self.getAdjVertices(vex1)) and (edge in self._edges)


    def addEdge(self, edge, weight=1):
        assert(len(edge) == 2)
        vex1, vex2 = edge

        if (self.checkEdge([vex1, vex2])) or (self.checkEdge([vex2, vex1])):
            raise KeyError('edge {} already exist in this graph'.format(edge))

        self.getVertex(vex1).addAdjVertex(vex2)
        self.getVertex(vex2).addAdjVertex(vex1)
        self._edges.append(Edge(edge, weight))


    def delEdge(self, edge):
        assert(len(edge) == 2)

        vex1, vex2 = edge
        if not self.checkEdge((vex1, vex2)):
            raise KeyError('edge {} cannot be found'.format(edge))

        self.getVertex(vex1).delAdjVertex(vex2)
        self.getVertex(vex2).delAdjVertex(vex1)
        self._edges.pop(self._edges.index(edge))


    def addVertex(self, vex):
        if vex in self._vertices:
            raise NameError('vertex {} already'.format(vex))
        self._vertices.append(Vertex(vex, []))


    def delVertex(self, vex):
        if vex not in self._vertices:
            raise NameError('vertex {} cannot be found'.format(vex))

        for v in self._vertices:
            if vex in v.adjVertices:
                v.delAdjVertex(vex)
        del_map = []
        for index, edge in enumerate(self._edges):
            if vex in edge.vertex_pair:
                del_map.append(index)

        self._edges = [i for j, i in enumerate(self._edges) if j not in del_map]
        self._vertices.pop(self._vertices.index(vex))

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
            tempReverseEdge = [node2, node1]

            #select another nodes if edge already exists or node1 equals to node2
            while tempEdge in edgePairList or tempReverseEdge in edgePairList or node1 == node2:
                node1 = random.choice(vertexNameList)
                node2 = random.choice(vertexNameList)
                tempEdge = [node1, node2]
                tempReverseEdge = [node2, node1]

            edgePairList.append(tempEdge)


        for i in range(0, edgeNo):
            weightList.append(random.randint(1,15))

        return Graph(vertexNameList, edgePairList, weightList)


