import unittest
from structure.config import *
from utils.variable import variable
from utils.executor import evaluate, execute, findMatchingObjInVar
import glb

class MyTestCase(unittest.TestCase):
    def setUp(self):
        glb.function_map.update(globals())
        x = Array([1,2,3,4])
        obj = variable('x', x)
        glb.variable_stack.append(['x',obj])

        y = Array([6,7,8,9])
        obj = variable('y', y)
        glb.variable_stack.append(['y',obj])


    def test_execute(self):
        sentence = "z = y[2] + len(y)"
        execute(sentence)
        print(glb.variable_stack[0][1])
        print(glb.variable_stack[1][1].var_obj.eleFlags)

    def test_execute2(self):
        sentence = "x[1] = {}"
        execute(sentence)


    def test_eval(self):
        exp = 'b[0]'
        dictionary = {'b': Array([1,2])}
        result = eval(exp, dictionary)
        print(result)

    def testFindMatchingObjInVar(self):
        obj = object()
        x = [[1,2,3],[4,{"b":2,"a":obj}], [6]]

        result = findMatchingObjInVar(obj, x)
        print(result)


if __name__ == '__main__':
    unittest.main()
