'''
Author: Fang Zhou
Date: 2015/8/13
Version: 1.0
Description: recursively execute the pseudo code.
'''

import sys
from module.config import *
from structure.config import *
from utils.executor import execute, evaluate
from visualize.plot import plot

import utils.parser as parser
import glb
import visualize.plot as plot

#module type
functionType = (functionmodule, )
loopType = (whilemodule, formodule, )
branchType = (ifelsemodule, )

def recursive(content, index, module):
    """
    recursively execute sentences

    Grammar structure:
    definition: Define variables or functions. Assignment statements are also considered as definition

    Expression: Operations

    Statement: Including if, while, for and repeat/until, break, continue, return.
    """
    if module.end_recursive:
        return
    else:
        #code compilation in progress
        if index < len(content):
            glb.current_line = module.line + index

            #empty line or comment line
            if not content[index].split("#")[0] or content[index].split("#")[0].isspace():
                index += 1
            else:
                #console output on server side
                # print("compile content: {}".format(content[index]))

                #lexicial analyze the statement
                grammar_type, tokenList, exeToken, param_list = parser.parse(content[index])

                #Case1: function definition
                if grammar_type == 'function_def':
                    lineCount = get_block_count(content, index)
                    module_content = content[index+1:index+lineCount+1]
                    func_name = param_list[0]
                    func_param_list = param_list[1]
                    glb.current_line += 1 #navigate to the next line
                    funcModule = functionmodule(func_name, func_param_list, module_content, glb.current_line)
                    module._func_inc(func_name, funcModule)
                    index += (lineCount+1)
                #Case2: expression
                elif grammar_type == 'expression':
                    from utils.consoleManager import stdoutIO

                    with stdoutIO() as s:
                        execute(exeToken)
                    consoleOutput = s.getvalue()
                    if consoleOutput:
                        glb.console_output.append(consoleOutput)

                    plot.plot()

                    index += 1
                #Case3: statement
                elif grammar_type == 'statement':
                    #continue, break, return

                    #3.1 return statement
                    if tokenList[0][1] == 'return':
                        try:
                            for item in reversed(glb.variable_stack):
                                if isinstance(item, functionmodule):
                                    item.return_list = evaluate(exeToken)
                                    break
                        except AttributeError:
                            raise Exception("SyntaxError: return statement must be used inside function.")

                        #set end_recursive to true
                        for item in reversed(glb.variable_stack):
                            if isinstance(item, functionmodule):
                                break
                            elif isinstance(item, basemodule):
                                item.setEnd()

                        # TODO plot.printVar() #print variable status before return

                        return #terminate the function

                    #3.2 break/continue statement
                    elif tokenList[0][1] == 'break' or tokenList[0][1] == 'continue':
                        for item in reversed(glb.variable_stack):
                            if isinstance(item, functionmodule):
                                raise Exception("Break/continue can only be used in while and for loops")

                            #terminate the modules inside loops
                            if isinstance(item, basemodule):
                                if not isinstance(item, loopType):
                                    item.setEnd()
                                else:
                                    item.setEnd()
                                    if tokenList[0][1] == 'continue':
                                        item.setContinue()
                                    break
                        #TODO plot.printVar() #print variable status
                        return

                    #3.3 if, while, for statement
                    else:
                        lineCount = get_block_count(content, index)
                        module_content = content[index+1:index+lineCount+1]

                        if tokenList[0][1] == 'if':
                            conditionList = [param_list[0]]
                            contentList = [module_content]

                            index += (lineCount+1)

                            if index < len(content):
                                grammar_type, tokenList, exeToken, param_list = parser.parse(content[index])

                                while len(tokenList) > 0 and tokenList[0][1] == 'else':
                                    lineCount = get_block_count(content, index)
                                    contentList.append(content[index+1: index+lineCount+1])
                                    index += (lineCount+1)
                                    conditionList.append(param_list[0])

                                    #continue looping
                                    if index >= len(content):
                                        break
                                    grammar_type, tokenList, exeToken, param_list = parser.parse(content[index])

                            ifModule = ifelsemodule(conditionList, contentList, glb.current_line)

                            ifModule.run()

                        elif tokenList[0][1] == 'for':
                            forModule = formodule(param_list, module_content, glb.current_line)
                            forModule.run()
                            index += (lineCount+1)

                        elif tokenList[0][1] == 'while':
                            whileModule = whilemodule(param_list[0], module_content, glb.current_line)
                            whileModule.run()
                            index += (lineCount+1)

                        else:
                            raise Exception("Unsupported keyword: {} in statement \"{}\"".format(tokenList[0][1], content[index]))

            #recursively compile the content
            recursive(content, index, module)


def get_block_count(content, index):
    '''
    Get the number of lines of this block.
    :param content: content of code
    :param index:start index
    :return: number of lines
    '''
    startSpace = len(content[index]) - len(content[index].lstrip())

    curIndex = index + 1
    while curIndex < len(content):
        #empty line or comment line. Attention: ''.isspace() == False
        if not content[curIndex].split("#")[0] or content[curIndex].split("#")[0].isspace():
            curIndex += 1
        else:
            curSpace = len(content[curIndex]) - len(content[curIndex].lstrip())
            if curSpace <= startSpace:
                curIndex -= 1
                break
            else:
                curIndex += 1

    return curIndex - index
