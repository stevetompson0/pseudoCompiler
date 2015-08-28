import glb, copy
from structure.matrix.Matrix import Matrix

class StringMatrix(Matrix):

    __name__ = 'StringMatrix'

    def __init__(self, rows, cols, fill=""):
        self.nrows = rows
        self.ncols = cols
        self._grid = [[fill for i in range(cols)] for j in range(rows)] #2D list
        self._preImage = copy.deepcopy(self._grid)
        self._eleFlags = [[glb.flag_dict['unchanged'] for i in range(cols)] for j in range(rows)] #2D list
        self._edges = []
        self._topheader = []
        self._leftheader = []

    @property
    def eleFlags(self):
        for row in range(0, len(self._grid)):
            for col in range(0, len(self._grid[row])):
                if self._preImage[row][col] != self._grid[row][col]:
                    self._eleFlags[row][col] = glb.flag_dict['changed']
        self._preImage = copy.deepcopy(self._grid)
        return self._eleFlags

    @property
    def edges(self):
        return self._edges

    @property
    def topheader(self):
        return self._topheader

    @property
    def leftheader(self):
        return self._leftheader

    def setTopHeader(self, header):
        '''
        :param header: String or list
        '''
        if len(header) > self.ncols:
            return

        self._topheader = []

        for i in range(0, len(header)):
            self._topheader.append(header[i])


    def setLeftHeader(self, header):
        if len(header) > self.nrows:
            return
        self._leftheader = []
        for i in range(0, len(header)):
            self._leftheader.append(header[i])

    def hasEdge(self, row1, col1, row2, col2):
        return [row1, col1, row2, col2] in self._edges or [row2, col2, row1, col1] in self._edges

    def addEdge(self, row1, col1, row2, col2):
        self._edges.append([row1, col1, row2, col2])

    def removeEdge(self, row1, col1, row2, col2):
        self._edges.remove([row1, col1, row2, col2])


    @staticmethod
    def FromList(l):
        """ Instantiates a new matrix object from a list of lists. """
        m = StringMatrix(len(l), len(l[0]))
        for rownum, row in enumerate(l):
            for colnum, element in enumerate(row):
                m[rownum][colnum] = element

        m._preImage = copy.deepcopy(m._grid)
        return m

    def resetFlags(self):
        self._eleFlags = [[glb.flag_dict['unchanged'] for i in range(self.ncols)] for j in range(self.nrows)] #2D list


    #generate a String Matrix randomly
    @classmethod
    def random(cls):
        import random

        cols = random.randint(glb.randomLowRange, glb.randomUpperRange)
        rows = random.randint(glb.randomLowRange, glb.randomUpperRange)

        matrixList = []
        for i in range(rows):
            matrixList.append(random.sample(range(100), cols))

        matrix = StringMatrix.FromList(matrixList)
        matrix.resetFlags()
        return matrix