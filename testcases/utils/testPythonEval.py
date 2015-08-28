import unittest
from structure.config import *
import sys

class MyTestCase(unittest.TestCase):
    '''
    Aims to test how lambda, exec, eval works.
    '''
    def test_lambda(self):
        functionMap = {}
        # for ele in globals():
        #     print(ele + ": " +  str(globals()[ele]))
        functionMap.update(globals())

        f1 = lambda x: x+1; print("fa")
        functionMap.update({'f1': f1})
        exec('y=f1(3)', functionMap)

        exec("z=y+1", functionMap)
        functionMap.update(globals())
        for ele in functionMap:
            if ele == "z":
                print(ele + ": " +  str(functionMap[ele]))

        exec("a=2")
        exec("b=a")
    #
    # def test_exec(self):
    #     x = {}
    #     exec("a=1")
    #     x = locals()
    #     for ele in x:
    #         print(x[ele])

    def test_variable(self):
        from utils.variable import variable
        x = variable('a', None)
        attr1 = getattr(x, 'var_name')
        attr2 = getattr(x, 'void')
        # attr3 = getattr(x, 'test')


        # print(hasattr(attr1, '__call__'))
        # print(hasattr(attr2, '__call__'))
        # print(dir(x))

    def test_attr(self):
        class A():
            def __init__(self, attr1):
                self.attr1 = attr1

            def set(self, val):
                self.attr1 = val

            def get(self):
                return self.attr1

        class B():
            def __init__(self, attr2):
                self.attr2 = attr2

        b = B("B")
        a = A(b)

        # a.get() = 2

        # x = getattr(a, "attr1")
        #
        # print(b.attr2)
        # setattr(x, "attr2", 4)
        # print(b.attr2)

        # c = a
        # d = c.attr1
        # e = d.attr2
        # se = "string"
        # print(b.attr2)

    def test_exec(self):
        pass

if __name__ == '__main__':
    unittest.main()
