'''
Author: Fang Zhou
Date: 2015/7/16
Version: 1.0
Description: execute input expression based on variable stack and function stack
'''
import glb
from utils.parser import lexical_analyze, keywords, opts, VARRANGE
from utils.variable import variable

equalToken = (opts['='], '=')
dotToken = (opts['.'], '.')

def execute(statement):
    '''
    :param statement: statement to be executed
    :return the value returned by the statement if any, otherwise return None
    New variables will be added to variable stack.

    Expression type: 1) variable definition 2) if, for, while statement's conditions 3) pure expression

    **********
    For right operand, we could invoke evaluate function directly.
    For left operand, we could invoke evaluate function for the parameters and indices.
    However we can not use evaluate function for the entire left operand because if the returned object of left operand is a string type,
    we can not change the object value by simply assign the right operand value to it.
    Eg. x = 4
    left = evaluate(x)
    right = evaluate(4)
    left = right
    x is not changed!
    '''
    tokenList = lexical_analyze(statement)

    #statement is an assignment. Left operand must be a variable
    #Three types of left operand:
    #1. object -> Need to store new variable to stack
    #2. object.function()
    #3. object[index/key] -> Need to record the index or key

    #if it is an assignment
    if equalToken in tokenList:
        indexOfEqual = tokenList.index(equalToken)
        leftOpTokens = tokenList[:indexOfEqual]
        rightOpTokens = tokenList[indexOfEqual+1:]

        #get string expression of right operand
        rightOpStr = ''
        for token in rightOpTokens:
            rightOpStr += token[1] + ' '

        #the object of the left operand
        leftObjectName = leftOpTokens[0][1]

        #variable is not defined yet
        if not containVariableInGlbStack(leftObjectName):
            #second or third type of left operand
            if len(leftOpTokens) > 1:
                raise Exception("\""+ leftObjectName + "\" is undefined in statement: " + statement)
            #first type of left operand
            else:
                rightOpValue = evaluate(rightOpStr)
                variableObj = variable(leftObjectName, rightOpValue)
                glb.variable_stack.append([leftObjectName, variableObj])

        #variable is defined previously
        else:
            variableInstance = getVariableFromGlbStack(leftObjectName) #get variable from global stack
            rightOpValue = evaluate(rightOpStr) #evaluate the right operand and get the value
            variableInstance.var_flag = glb.flag_dict['changed']

            #single variable, store in the global stack directly
            if len(leftOpTokens) == 1:
                variableInstance.var_obj = rightOpValue
            else:
                #analyze token before ".", find indices visited. Format: obj[index/key]...[index/key]
                leftOpObject = variableInstance.var_obj
                storeVisitedIndex(leftOpTokens)

                #compile until the last "." or "[".  To split the left operand into 2 parts, the first part is non-primitive and second part is primitive part

                #find the index of last '.' OR '['
                index = 0
                splitIndex = 0
                while index < len(leftOpTokens):
                    if leftOpTokens[index][1] == '.' or leftOpTokens[index][1] == '[':
                        splitIndex = index
                    index += 1

                index = 1 #reset index
                exp = ''
                token = '' #single token
                currentObject = leftOpObject #object compiled until now

                while index < len(leftOpTokens):
                    token = leftOpTokens[index][1]
                    #attribute or function call
                    if token == '.':
                        index += 1
                        token = leftOpTokens[index][1]
                        if token not in dir(currentObject):
                            raise Exception("AttributeError: \'" + leftObjectName + "\' object has no attribute \'" + token + "\'")
                        else:
                            if index >= splitIndex:
                                setattr(currentObject, token, rightOpValue)
                            else:
                                currentObject = getattr(currentObject, token)
                    #function call
                    elif token == '(':
                        bracket_stack = []
                        bracket_stack.append(token)
                        isMultipleParam = False

                        while index < len(leftOpTokens)-1 and bracket_stack:
                            index += 1
                            token = leftOpTokens[index][1]
                            #check if it is multiple parameters
                            if token == ',' and len(bracket_stack) == 1:
                                isMultipleParam = True

                            if token == '(':
                                bracket_stack.append(token)
                            elif token == ')':
                                bracket_stack.pop()
                            if bracket_stack:
                                exp += token
                        paramResult = evaluate(exp)

                        if isMultipleParam:
                            currentObject = currentObject(*paramResult)#execute the function, paramResult may be a tuple with multiple parameters
                        else:
                            currentObject = currentObject(paramResult)
                    #indices or keys
                    elif token == '[':
                        bracket_stack = []
                        bracket_stack.append(token)

                        while index < len(leftOpTokens)-1 and bracket_stack:
                            index += 1
                            token = leftOpTokens[index][1]
                            if token == '[':
                                bracket_stack.append(token)
                            elif token == ']':
                                bracket_stack.pop()
                            if bracket_stack:
                                exp += token
                        paramResult = evaluate(exp)
                        if index >= splitIndex:
                            currentObject[paramResult] = rightOpValue
                        else:
                            currentObject = currentObject[paramResult]#execute the function
                    else:
                        raise Exception("Invalid syntax at " + token + " in statement " + statement)
                    token = ''
                    exp = ''
                    index += 1

        storePointer(leftOpTokens, rightOpTokens)
    else:
        evaluate(statement)



def evaluate(expression):
    '''
    :param expression: the expression argument is parsed and evaluated.
    :return: the result of the evaluated expression
    Similar to python eval function. The evaluate function only compile a single expression and returns the value of the expression.
    Syntax errors are reported as exceptions.

    Todo: in this version, we keep using python eval(). Will change in next version.
    '''

    tokenList = lexical_analyze(expression)
    #Add Array or Dict to array definition or dict definition
    #E.g. [1,[1,2]] => Array([1,Array[1,2]])

    index = 0
    token = ''
    modifiedExp = ''

    bracket_stack = [] #stack of '[', ']'
    brace_stack = [] #stack of '{', '}'

    while index <len(tokenList):
        token = tokenList[index][1]

        #avoid case like x[index] and [x[1], 2, 3]
        #1. '[' is part of array definition
        if token == '[' and (index ==0 or (index > 0 and tokenList[index-1][0] not in VARRANGE and tokenList[index-1][1] not in [']', ')'])):
            modifiedExp += "Array(["
        #2. '[' is used for index
        elif token == '[':
            modifiedExp += token
            bracket_stack.append('[')
        elif token == ']':
            #3. ']' is part of index visit
            if bracket_stack:
                bracket_stack.pop()
                modifiedExp +=  token
            #4. ']' is part of array definition
            else:
                modifiedExp += "])"
        #5. '{}' is dictionary definition
        elif token == '{':
            modifiedExp += "Dict({"
        elif token == '}':
            modifiedExp += "})"
        #6. other cases
        else:
            modifiedExp += token

        modifiedExp += ' '
        index += 1

    expression = modifiedExp

    #TODO: be careful about variable scope, to be tested later
    #step1: store all variable in global stack to a dictionary, start from bottom of stack.
    from module.basemodule import basemodule
    varDict = {}
    for variablePair in glb.variable_stack:
        if not isinstance(variablePair, basemodule):
            varDict[variablePair[0]] = variablePair[1].var_obj

    #step2: use python eval
    result = eval(expression, glb.function_map, varDict)
    return result

def containVariableInGlbStack(var_name):
    '''
    check whether variable exist in global variable stack or not
    :param var_name: variable name
    :return: True if exist, False otherwise
    '''

    #start from the bottom of the stack, local variables first.
    #No need =>Only check variable in current function scope and global scope.
    from module.basemodule import basemodule
    from module.functionmodule import functionmodule

    # #1. check function scope first
    # for variablePair in reversed(glb.variable_stack):
    #     if isinstance(variablePair, basemodule):
    #         if isinstance(variablePair, functionmodule):
    #             break
    #     else:
    #         if var_name == variablePair[0]: #variablePair: [var_name, variable_obj]
    #             return True
    #
    # #2. check global scope
    # for variablePair in glb.variable_stack:
    #     if isinstance(variablePair, basemodule):
    #         if isinstance(variablePair, functionmodule):
    #             break
    #     else:
    #         if var_name == variablePair[0]: #variablePair: [var_name, variable_obj]
    #             return True

    for variablePair in reversed(glb.variable_stack):
        if not isinstance(variablePair, basemodule) and var_name == variablePair[0]:
            return True

    return False

def getVariableFromGlbStack(var_name):
    '''
    get first matching variable from global stack, iterate from the top of the stack
    :param var_name: variable name
    :return: object of type "variable" class
    '''

    from module.basemodule import basemodule
    from module.functionmodule import functionmodule

    # #1. check function scope first
    # for variablePair in reversed(glb.variable_stack):
    #     if isinstance(variablePair, basemodule):
    #         if isinstance(variablePair, functionmodule):
    #             break
    #     else:
    #         if var_name == variablePair[0]:
    #             return variablePair[1]
    #
    # #2. check global scope first
    # for variablePair in glb.variable_stack:
    #     if isinstance(variablePair, basemodule):
    #         if isinstance(variablePair, functionmodule):
    #             break
    #     else:
    #         if var_name == variablePair[0]:
    #             return variablePair[1]

    for variablePair in reversed(glb.variable_stack):
        if not isinstance(variablePair, basemodule) and var_name == variablePair[0]:
            return variablePair[1]
    return None

def getMatchingObject(obj):
    '''
    Find matching object from global variable stack. Start from bottom of stack.
    a <- b <- c, we want to find c -> a, so start from the bottom of stack
    :param obj:
    :return: return object of type "variable" if found, return None otherwise.
    '''
    from module.basemodule import basemodule

    for variablePair in glb.variable_stack:
        if not isinstance(variablePair, basemodule) and obj is variablePair[1].var_obj:
            return variablePair[1]
    return None


def storeVisitedIndex(tokens):
    '''
    Find the indices or keys visited of one variable. Only care about the indices before "."
    :param tokens: tokens of the expression. Expression format: object[index/key]...[index/key].
        index/key could be expression!
    :return: None
    '''
    #ignore the tokens after "."
    firstDotIndex = len(tokens) #init value
    if dotToken in tokens:
        firstDotIndex = tokens.index(dotToken)

    objectName = tokens[0][1]
    variableInstance = getVariableFromGlbStack(objectName) #get variable from global stack

    if variableInstance is None:
        raise Exception("\""+ objectName + "\" is undefined in statement: " + str(tokens))

    indexList = []
    bracketStack = []
    token = ''
    ch = ''
    i = 1
    while i < firstDotIndex:
        ch = tokens[i][1]
        if ch == '[':
            bracketStack.append(ch)
            while bracketStack and i < firstDotIndex-1:
                i += 1
                ch = tokens[i][1]
                if ch == '[':
                    bracketStack.append(ch)
                elif ch == ']':
                    bracketStack.pop()
                if bracketStack:
                    token += ch + ' '
            indexList.append(evaluate(token))
        else:
            raise Exception("Brackets not closed in statement: " + str(tokens))
        token = ''
        i += 1
    variableInstance.indexList = indexList

# def storePointer(leftOpTokens, rightOpTokens):
#     '''
#     Version 1: Only deal with pointers in format: objectA = objectB, objectA = objectB[].
#     :param leftOpTokens: tokens of left operand
#     :param rightOpTokens: tokens of right operand
#     '''
#     if len(leftOpTokens) != 1:
#         return
#     leftVar = getVariableFromGlbStack(leftOpTokens[0][1])
#     rightVar = getVariableFromGlbStack(rightOpTokens[0][1])
#
#     if leftVar is None or rightVar is None:
#         return
#
#     i = 1
#     indexList = []
#     bracketStack = []
#     token = ''
#     ch = ''
#
#     while i < len(rightOpTokens):
#         ch = rightOpTokens[i][1]
#         if ch == '[':
#             bracketStack.append(ch)
#             while bracketStack and i < len(rightOpTokens)-1:
#                 i += 1
#                 ch = rightOpTokens[i][1]
#                 if ch == '[':
#                     bracketStack.append(ch)
#                 elif ch == ']':
#                     bracketStack.pop()
#                 if bracketStack:
#                     token += ch + ' '
#             indexList.append(evaluate(token))
#         else:
#             return #right operand does not follow the format
#         token = ''
#         i += 1
#
#     if not isPrimitiveType(leftVar.var_obj):
#         leftVar.pointer = rightVar.var_name #should be name, not object
#         leftVar.pointerIndexList = indexList

def storePointer(leftOpTokens, rightOpTokens):
    '''
    Version 2: check the global variable stack to find the matching object, and check whether leftOpToken matches
    the element inside the object if object is list or dictionary type.

    Limitation: The left operand must be a single variable!!! (Difficulties in front animation)

    :param leftOpTokens: tokens of left operand
    :param rightOpTokens: tokens of right operand. Not used.
    '''
    from module.basemodule import basemodule
    if len(leftOpTokens) != 1:
        return
    leftVar = getVariableFromGlbStack(leftOpTokens[0][1])

    #leftVar should be stored inside global variable stack already after finishing execute function
    if leftVar is None or isPrimitiveType(leftVar.var_obj):
        return

    #traverse the global variable stack, to find the most original object, we start from the bottom of global stack
    # for variablePair in reversed(glb.variable_stack):
    for variablePair in glb.variable_stack:
        if not isinstance(variablePair, basemodule):
            varInstance = variablePair[1]

            #case 1: varInstance.var_obj is the same as leftVar.var_obj and variable name should be different.
            #If the variable name are the same. var(local) = var(global) is impossible!
            if varInstance.var_obj is leftVar.var_obj:
                if varInstance.var_name != leftVar.var_name:
                    leftVar.pointer = varInstance.var_name
                    break
            #case 2: leftVar is the element of varInstance.var_obj. varInstance is list or dictionary type.
            elif isinstance(varInstance.var_obj, list) or isinstance(varInstance.var_obj, dict):
                isFound, indexList = findMatchingObjInVar(leftVar.var_obj, varInstance.var_obj)
                if isFound:
                    leftVar.pointer = varInstance.var_name
                    leftVar.pointerIndexList = indexList
                    break

def findMatchingObjInVar(obj, targetObj, indexList=[]):
    '''
    Traverse through the dictionary or list to find out the matching object.
    :param obj: input object
    :param targetObj: object to be traversed (list or dictionary type).
    :param indexList: list store the indices which is used to find the input object in targetObj.
    :return isFound, indexList.
    '''
    from copy import deepcopy
    if obj is targetObj:
        return True, indexList

    # #reach the bottom
    # if not isinstance(targetObj, list) and not isinstance(targetObj, dict):
    #     if obj is targetObj:
    #         return True, indexList
    #     else:
    #         return False, indexList
    if isinstance(targetObj, list):
        for index, element in enumerate(targetObj):
            indexList.append(index)
            isFound, returnList = findMatchingObjInVar(obj, element, indexList)
            if not isFound:
                indexList.pop()
            else:
                return True, indexList
    elif isinstance(targetObj, dict):
        for key in targetObj:
            indexList.append(key)
            isFound, returnList = findMatchingObjInVar(obj, targetObj[key], indexList)
            if not isFound:
                indexList.pop()
            else:
                return True, indexList

    return False, indexList


def isPrimitiveType(var):
    '''
    :param var: variable
    :return: return True if variable is primitiveType, return False otherwise
    '''
    primitive = (int, float, str, bool)
    # return isinstance(var, primitive) or var == None #does not work for StringMatrix
    return type(var) in primitive or var == None

