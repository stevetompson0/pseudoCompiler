'''
Author: Fang Zhou
Date: 2015/5/6
Version: 1.0
Description:
1) Lexical analysis: convert input code into token pairs. Format: <token number, token name>
2) Syntax analysis:  analyze the tokens, check the syntax and return
3) Semantic analysis: check variable use (defined before referencing...). This part will be implemented by execute function

'''

import sys
import glb

# 1. variables ID: 0
# 2. function ID or Data structure class： 1
# 3. constants: 2
# 3. keywords: 3 ~ 40
# 4, operators: 41 ~ infinity

#statement range: 3 ~ 11
VARRANGE = range(0, 3)
STATEMENTRANGE = range(3, 12)

keywords = {'if':       3,
            'else':     4,
            'for':      5,
            'while':    6,
            'break':    7,
            'continue': 8,
            'return':   9,
            'repeat':   10,
            'until':    11,

            'function': 12,
            'is':       13,
            'in':       14,
            'or':       15,
            'and':      16,
            'not':      17,
            'to':       18,
            'step':     19,
        }

#TODO some operators are not used or defined
opts = {'+':            41,
        '-':            42,
        '*':            43,
        '/':            44,
        '<':            45,
        '<=':           46,
        '>':            47,
        '>=':           48,
        '<>':           49,
        '!=':           50,
        '=':            51,
        '==':           52,
        ';':            53,
        '(':            54,
        ')':            55,
        '&':            56,
        '&&':           57,
        '|':            58,
        '||':           59,
        '^':            60,
        '%':            61,
        '>>':           62,
        '<<':           63,
        ',':            64,
        '//':           65,
        '[':            66,
        ']':            67,
        '+=':           68,
        '-=':           69,
        '->':           70,
        '++':           71,
        '--':           72,
        '^':            73, #exponent, same as '**' in python
        '.':            74, #function call or attribute
        '{':            75, #dictionary left brackets
        '}':            76, #dictionary right brackets
        ':':            77, #dictionary pair
    }

def lexical_analyze(sentence):
    '''

    :param sentence: one line of input source code
    :return: tuple of token pairs <token index, token name>

    Five kinds of syntax:
    1. Keywords
    2. Operators
    3. Variable name
    4. Function name
    5. Constants
    '''

    token = ''
    tokenList = []

    #simply remove all the strings after "#"; "#" stands for annotation
    sentence = sentence.split("#")[0]

    #Transform the sentence. "+=", "-=", "++", "--", "->"
    sentence = sentence.replace("->", "=")
    while "+=" in sentence or "-=" in sentence or "++" in sentence or "--" in sentence:
        if "+=" in sentence:
            splitList = sentence.split("+=")
            sentence = splitList[0] + "=" + splitList[0] + "+" + splitList[1]
        elif "-=" in sentence:
            splitList = sentence.split("-=")
            sentence = splitList[0] + "=" + splitList[0] + "-" + splitList[1]
        #Assume "++" and "--" only appear at the end of expression
        elif "++" in sentence:
            splitList = sentence.split("++")
            sentence = splitList[0] + "=" + splitList[0] + "+ 1"
        elif "--" in sentence:
            splitList = sentence.split("--")
            sentence = splitList[0] + "=" + splitList[0] + "- 1"

    index = 0
    bracket_stack = []

    while index < len(sentence):
        ch = sentence[index] #character

        #if character is empty (' ', '\t', '\n')
        if ch.isspace():
            index += 1
            continue

        #if is alphabet (A-Z, a-z)
        if ch.isalpha():
            #get string consisting of [a-zA-Z0-9_]，in other words: valid variable or function name
            while (ch.isalpha() or ch.isdigit() or ch == '_') and index < len(sentence):
                token += ch
                index += 1
                if index < len(sentence):
                    ch = sentence[index]

            #skip the spaces
            while ch.isspace() and index <len(sentence):
                index += 1
                if index < len(sentence):
                    ch = sentence[index]

            if token in keywords:
                tokenList.append((keywords.get(token), token))
            else:
                #token is function name
                if ch == '(' :
                    tokenList.append((1, token))
                #token is data structure class in glb.function_list
                elif token in glb.function_map:
                    tokenList.append((1, token))
                #token is variable name or other things
                else:
                    tokenList.append((0, token))
            index -= 1

            # #function definition or function calls, include the parameters in brackets
            # if ch == '(':
            #     bracket_stack.append(ch)
            #     if token in keywords:
            #         tokenList.append((keywords.get(token), token))
            #         tokenList.append((opts.get(ch), ch))
            #         bracket_stack.pop() #ignore the brackets, store the token pair
            #     else:
            #         while bracket_stack and index < len(sentence):
            #             token += ch
            #             index += 1
            #             if index < len(sentence):
            #                 ch = sentence[index]
            #
            #             if ch == '(':
            #                 bracket_stack.append(ch)
            #             elif ch == ')':
            #                 bracket_stack.pop()
            #         token += ch
            #         tokenList.append((2, token))

            # elif ch == '[':
            #     bracket_stack.append(ch)
            #     while bracket_stack and index < len(sentence):
            #         token += ch
            #         index += 1
            #         if index < len(sentence):
            #             ch = sentence[index]
            #
            #         if ch == '[':
            #             bracket_stack.append(ch)
            #         elif ch == ']':
            #             bracket_stack.pop()
            #     token += ch
            #     tokenList.append((1, token))

            # else:
            #     index -= 1
            #     if token in keywords:
            #         tokenList.append((keywords.get(token), token))
            #     else:
            #         tokenList.append((1, token))

        #if character is digit
        elif ch.isdigit():
            #get the entire number
            while (ch.isdigit() or ch == '.') and index < len(sentence):
                token += ch
                index += 1
                if index < len(sentence):
                    ch = sentence[index]

            index -= 1 #index points to the last visited character
            tokenList.append((2, token))

        #if character is single quote
        elif ch == '\'':
            token += ch
            index += 1
            ch = sentence[index]

            #simply read until the next single quote
            while ch != '\'' and index < len(sentence):
                token += ch
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
            token += ch
            tokenList.append((2,token))

        #if character is double quotes
        elif ch == '\"':
            token += ch
            index += 1
            ch = sentence[index]

            #simply read until the next double quote
            while ch != '\"' and index < len(sentence):
                token += ch
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
            token += ch
            tokenList.append((2,token))

        #operators
        else:
            token += ch

            if ch == '<':
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
                    #<=, <>, <<
                    if ch in ('=', '>', '<'):
                        token += ch
                    else:
                        index -= 1
            elif ch == '>':
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
                    #>=, >>
                    if ch in ('=', '>'):
                        token += ch
                    else:
                        index -= 1
            elif ch == '!':
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
                    # "!="
                    if ch == "=":
                        token += ch
                    else:
                        index -= 1
            elif ch == "=":
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
                    # "=="
                    if ch == "=":
                        token += ch
                    else:
                        index -= 1
            elif ch == "&":
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
                    # "&&"
                    if ch == "&":
                        token += ch
                    else:
                        index -= 1
            elif ch == "|":
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
                    # "||"
                    if ch == "|":
                        token += ch
                    else:
                        index -= 1
            elif ch == "+":
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
                    # "+=", "++",
                    if ch in ('=', '+'):
                        token += ch
                    else:
                        index -= 1
            elif ch == "-":
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
                    # "-=", "--", "->"
                    if ch in ('=', '-', '>'):
                        token += ch
                    else:
                        index -= 1
            elif ch == "/":
                index += 1
                if index < len(sentence):
                    ch = sentence[index]
                    # "//"
                    if ch in ('/',):
                        token += ch
                    else:
                        index -= 1
            if token in opts:
                tokenList.append((opts.get(token), token))
            else:
                raise Exception("Invalid operator \"" + str(token) +"\" in statement: " + sentence)

        index += 1
        token = ''
    return tuple(tokenList)



def parse(sentence):
    '''
    :param sentence: one line of the input source code
    :return:
    1. grammar_type: 'function_def', 'expression', 'statement'.  'variable_def' is regarded as expression
    2. tokenList
    3. exeToken: executable tokens for execute function use
    4. param_list: Due to grammar_type.
        If block is var definition,         param_list = [var_name]
        If block is function definition,    param_list = [func_name, function_parameter_tuple]
        if block is if or while statement,  param_list = [condition_expression]
        if block is for statement,          param_list = [iterator_variable_name, iterator_list, range_var]
                                                e.g 'for i = 1 to 10, step 1'
                                                param_list = ['i', (1, 2, 3, ..., 10), None]
                                                'for i in X'
                                                param_list = ['i', X, 'X']
    '''

    grammar_type = ''
    exeToken = ''
    param_list = []

    #lexical analyze the input statement
    tokens = lexical_analyze(sentence)

    if tokens:
        #case 1: function definition. E.g. function insert(param)
        if tokens[0][1] == 'function':
            grammar_type = 'function_def'
            #leave exeToken empty

            function_name, function_param = function_analyze(tokens[1:])
            param_list = [function_name, function_param]

        elif tokens[0][0] == 1:
            #case 2: variable definition. E.g. Stack s = [1,2]
            if tokens[1][0] == 0:
                grammar_type = 'expression'
                var_type = tokens[0][1]
                var_name = tokens[1][1]
                param_list = [var_name]
                exeToken = var_name + ' = ' + var_type

                if len(tokens) == 2:
                    exeToken += "()"
                else:
                    if tokens[2][1] == '=':
                        exeToken += '('
                        for indx in range(3, len(tokens)):
                            exeToken += tokens[indx][1] + ' '
                        exeToken += ')'
            #case 3: expression
            else:
                grammar_type = 'expression'
                #leave param_list empty
                for token in tokens:
                    exeToken += token[1] + ' ' #to remove unnecessary spaces, we do not use exeToken = sentence

        #case 4: statements
        elif tokens[0][0] in STATEMENTRANGE:
            grammar_type = 'statement'

            try:
                #case 4.1: for loop
                #for statement have two types:
                # 1. for [var_name] in [iter_list]
                # 2. for [var_name] = [startpos] to [endpos] step [step]
                if tokens[0][1] == 'for':
                    var_name = tokens[1][1]
                    loop_range = None #[iter_list]
                    range_var_name = ""

                    from utils.executor import evaluate
                    #first type
                    if tokens[2][1] == 'in':
                        range_exp = ''.join([token[1] for token in tokens[3:]]) #string expression of the range. In other words, [iter_list] string
                        loop_range = evaluate(range_exp)
                        range_var_name = range_exp
                    #second type
                    elif tokens[2][1] == '=':
                        exp_index = 3

                        #get start position
                        start_exp = ''
                        while exp_index < len(tokens) and tokens[exp_index][1] != 'to':
                            start_exp += tokens[exp_index][1] + ' '
                            exp_index += 1
                        startPos = evaluate(start_exp)

                        #skip 'to'
                        exp_index += 1

                        #get end position
                        end_exp = ''
                        while exp_index < len(tokens) and tokens[exp_index][1] != 'step':
                            end_exp += tokens[exp_index][1] + ' '
                            exp_index += 1
                        endPos = evaluate(end_exp)

                        #get step
                        exp_index += 1 #skip 'step'
                        step = 1 #default value
                        if exp_index < len(tokens):
                            step_exp = ''
                            while exp_index < len(tokens):
                                step_exp += tokens[exp_index][1] + ' '
                                exp_index += 1
                            step = evaluate(step_exp)

                        loop_range = range(startPos, endPos, step)
                    else:
                        raise Exception("Invalid for loop syntax: " + sentence)
                    param_list = [var_name, loop_range, range_var_name]

                # besides for statement
                else:
                    #get judge condition
                    if tokens[0][0] in STATEMENTRANGE:
                        for token in tokens[1:]:
                            #deal with cases like: else if
                            if token[0] in STATEMENTRANGE:
                                continue
                            #     raise Exception("Unacceptable: More than one condition statement in one line. E.g if XX else XX")
                            exeToken += token[1] + ' '

                        #cases like return, and so on
                        if exeToken == '':
                            exeToken = 'True'
                        param_list = [exeToken]
                    else:
                        raise Exception("Invalid syntax find in parser step: " + sentence)

            except Exception:
                raise

        #all other situations?!
        else:
            grammar_type = 'expression'
            #leave param_list empty
            for token in tokens:
                exeToken += token[1] + ' ' #to remove unnecessary spaces, we do not use exeToken = sentence

    return grammar_type, tokens, exeToken, param_list


def function_analyze(tokenList):
    '''
    :param tokenList: eg. insert ( param1 ,  param2 , ... )
    :return:function name, parameter list
    '''

    #At least should have function_name, left_bracket, right_bracket
    if len(tokenList) < 3 or tokenList[1][1] != '(' or tokenList[-1][1] != ')':
        raise Exception("Invalid function definition: " + str(tokenList))

    function_name = tokenList[0][1].strip()
    param_list = []

    #skip the brackets and commas
    for token in tokenList[2:-1]:
        if token[1] != ',':
            param_list.append(token[1])

    #apply strip to each element
    param_list = list(map(str.strip, param_list))

    return function_name, tuple(param_list)






















