import unittest
from structure.config import *


class MyTestCase(unittest.TestCase):
    def test_dict(self):
        x = Dict()
        x["A"] = 1
        x["B"] = 2
        x["C"] = 4
        x["A"] = 5
        print(x)
        print(x.eleFlags)

        x.pop("A")
        print(x)
        print(x.eleFlags)

        y = {"D": 8}
        x.update(y)
        print(x)
        print(x.eleFlags)

        x.resetFlags()
        print(x)
        print(x.eleFlags)

        x.clear()
        print(x)
        print(x.eleFlags)

        z = Dict.random()
        print(z)
        print(z.eleFlags)

        print(z.__name__)

        #self.assertEqual(True, False)

    def test_key(self):
        x = Dict({'a': 1, 'b': 2})
        x['a'] = 3
        print(x)
        print(x.eleFlags)

        y = x['a']
        print(x)
        print(x.eleFlags)



if __name__ == '__main__':
    unittest.main()
