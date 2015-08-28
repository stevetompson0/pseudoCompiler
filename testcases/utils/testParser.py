import unittest
import utils.parser as parser
from structure.config import *
import glb

class MyTestCase(unittest.TestCase):
    def setUp(self):
       glb.function_map.update(globals())

    def test_lexical(self):
        # sentence = "if obj.get(x)[1] < a[1]"
        # x = parser.lexical_analyze(sentence)
        #
        # sentence = "if obj.get(x).get(y) < a[1]"
        # x = parser.lexical_analyze(sentence)
        # print(x)

        sentence = "x-> y"
        x = parser.lexical_analyze(sentence)
        print(x)

    def test_parse2(self):
        sentence = "return x*y"
        gram, tokenList, exeToken, param_list = parser.parse(sentence)
        print(gram)
        print(tokenList)
        print(exeToken)
        print(param_list)

    def test_parse3(self):
        sentence = "nodes = graphFromParam.V #set"
        gram, tokenList, exeToken, param_list = parser.parse(sentence)
        print(gram)
        print(tokenList)
        print(exeToken)
        print(param_list)

    def test_parse4(self):
        sentence = "for i = 0 to 9 step 2"
        gram, tokenList, exeToken, param_list = parser.parse(sentence)
        print(gram)
        print(tokenList)
        print(exeToken)
        print(param_list)

    def test_parse5(self):
        sentence = "else if y < 0"
        gram, tokenList, exeToken, param_list = parser.parse(sentence)
        print(gram)
        print(tokenList)
        print(exeToken)
        print(param_list)

    def test_parse(self):
        #Test1: function
        sentence = "function sort(array)"
        gram, tokenList, exeToken, param_list = parser.parse(sentence)
        self.assertEquals(gram, 'function_def')
        self.assertEquals(tokenList, ((12, 'function'), (1, 'sort'), (54, '('), (0, 'array'), (55, ')')))
        self.assertEquals(param_list, ['sort', ('array',)])

        sentence = "function sort()"
        gram, tokenList, exeToken, param_list = parser.parse(sentence)
        print(len(param_list[1]))

        #Test2: variable definition in TYPE VAR = XXX format
        sentence = "Stack x = [1,2]"
        gram, tokenList, exeToken, param_list = parser.parse(sentence)
        self.assertEquals(gram, 'variable_def')
        self.assertEquals(exeToken, 'x = Stack([ 1 , 2 ] )')
        self.assertEquals(tokenList, ((1, 'Stack'), (0, 'x'), (51, '='), (66, '['), (2, '1'), (64, ','), (2, '2'), (67, ']')))
        self.assertEquals(param_list, ['x'])

        #Test3: variable definition expression
        sentence = "x = 'fang'"
        gram, tokenList, exeToken, param_list = parser.parse(sentence)
        self.assertEquals(gram, 'expression')
        self.assertEquals(exeToken, "x = 'fang' ")
        self.assertEquals(tokenList, ((0, 'x'), (51, '='), (2, "'fang'")))
        self.assertEquals(param_list, [])

        #Test4: statements:for loop
        sentence = "for x in range(4)"
        gram, tokenList, exeToken, param_list = parser.parse(sentence)
        self.assertEquals(gram, 'statement')
        self.assertEquals(exeToken, "")
        self.assertEquals(tokenList, ((5, 'for'), (0, 'x'), (14, 'in'), (1, 'range'), (54, '('), (2, '4'), (55, ')')))
        # execute function not finished yet
        # self.assertEquals(param_list, ['x', 0])

        sentence = "for x = 0 to 9"
        # gram, tokenList, exeToken, param_list = parser.parse(sentence)
        # self.assertEquals(gram, 'statement')
        # self.assertEquals(exeToken, "")
        # self.assertEquals(tokenList, ((5, 'for'), (0, 'x'), (51, '='), (2, '0'), (18, 'to'), (2, '9')))
        # #execute function not finished yet
        # self.assertEquals(param_list, ['x', range(0, 0)])
        #
        sentence = "for x = 0 to 9 step 2"
        print(parser.lexical_analyze(sentence))
        # # gram, tokenList, exeToken, param_list = parser.parse(sentence)
        # # self.assertEquals(gram, 'statement')
        # # self.assertEquals(exeToken, "")
        # # self.assertEquals(tokenList, ((5, 'for'), (0, 'x'), (51, '='), (2, '0'), (18, 'to'), (2, '9'), (19, 'step'), (2, '2')))
        # #execute function not finished yet
        # # self.assertEquals(param_list, ['x', range(0, 9, 2)])
        #
        #
        sentence = "while x < 9"
        gram, tokenList, exeToken, param_list = parser.parse(sentence)
        self.assertEquals(gram, 'statement')
        self.assertEquals(exeToken, "x < 9 ")
        self.assertEquals(tokenList, ((6, 'while'), (0, 'x'), (45, '<'), (2, '9')))
        #execute function not finished yet
        self.assertEquals(param_list, ["x < 9 "])
        #
        # sentence = "if x in range(9)"
        # gram, tokenList, exeToken, param_list = parser.parse(sentence)
        # self.assertEquals(gram, 'statement')
        # self.assertEquals(exeToken, "x in range(9) ")
        # self.assertEquals(tokenList, ((3, 'if'), (1, 'x'), (14, 'in'), (2, 'range(9)')))
        # #execute function not finished yet
        # self.assertEquals(param_list, ["x in range(9) "])
        #
        # # sentence = "return x, y" #do not support this kind of syntax
        # sentence = "return x"
        # gram, tokenList, exeToken, param_list = parser.parse(sentence)
        # self.assertEquals(gram, 'statement')
        # self.assertEquals(exeToken, "x ")
        # #execute function not finished yet
        # self.assertEquals(param_list, ["x "])




if __name__ == '__main__':
    unittest.main()
