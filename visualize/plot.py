'''
Author: Fang Zhou
Date: 2015/8/10
Version: 1.0
Description: store variable information inside dictionary for JSON output.
'''

from structure.config import *
from module.config import *
import glb, re

SPEC_TYPES = (str, PqueuePair, Vertex, Edge, dict)

def resetFlagInStack():
    '''
    Reset all the modification flags in variable stack
    '''

    for item in glb.variable_stack:
        if not isinstance(item, basemodule):
            variableObj = item[1]
            variableObj.var_flag = glb.flag_dict['unchanged']

            if 'resetFlags' in dir(variableObj.var_obj):
                variableObj.var_obj.resetFlags()

def plot():
    '''
    store all variables' information inside a dictionary for JSON output.
    '''
    glb.json_dict['statement_{}'.format(glb.step)] = status_dict()
    resetFlagInStack()
    glb.step += 1


def status_dict():
    '''
    Store all the variables' information inside a dictionary.
    :return: a dictionary which contains all the information until one statement
    '''

    sdict = {}
    sdict['current_line'] = glb.current_line+1#current_line start from 0
    sdict['current_content'] = glb.contents[glb.current_line]
    #if we do not add formatter, console output of all statements are the same. Reference to the same object
    sdict['console'] = formatter(glb.console_output)

    #store variables according to function call depth
    varDictByDepth = {}
    depth = 0 #depth start from 1, no need of glb.funcall_depth


    for item in glb.variable_stack:
        if isinstance(item, functionmodule) or isinstance(item, glbmodule):
            depth += 1
            varDictByDepth["depth_{}".format(depth)] = []
        elif isinstance(item, basemodule):
            pass
        else:
            newVar = {}
            newVar['name'] = item[0]
            varInstance = item[1]
            newVar['type'] = varInstance.var_obj.__class__.__name__ #Bad!!!
            newVar['varFlag'] = varInstance.var_flag
            newVar['index'] = formatter(list_scanner(varInstance.indexList))
            newVar['pointer'] = str(varInstance.pointer) #pointer is the object name
            newVar['pointerIndex'] = formatter(list_scanner(varInstance.pointerIndexList))
            newVar['value'] = formatter(varInstance.var_obj)

            for attrName in dir(varInstance.var_obj):
                attr = getattr(varInstance.var_obj, attrName)
                if (not hasattr(attr, '__call__')) and (not re.search(r'^_', attrName)):
                    if not isinstance(attr, SPEC_TYPES) and hasattr(attr, '__iter__'):
                        newVar[attrName] = formatter(list_scanner(attr))
                    elif isinstance(attr, Vertex):
                        newVar[attrName] = trans_vex(attr)
                    elif isinstance(attr, Edge):
                        newVar[attrName] = trans_edge(attr)
                    else:
                        newVar[attrName] = formatter(attr)
            varDictByDepth["depth_{}".format(depth)].append(newVar)

    sdict['vars'] = varDictByDepth
    return sdict

def trans_vex(vex):
    '''
    format vertex's json output.
    :param vex: Graph Vertex.
    :return:
    '''
    return {
        'value': formatter(vex.value),
        'color': formatter(vex.color),
        'adjs': formatter(vex.adjVertices)
    }

def trans_edge(edge):
    '''
    format edges' json output.
    :param edge: Graph Edge
    :return:+
    '''
    return {
        'start': formatter(edge.start),
        'end': formatter(edge.end),
        'color': formatter(edge.color),
        'weight': formatter(edge.weight)
    }

def list_scanner(objList):
    '''
    Format the object output inside list. E.g. vertices list.
    :param objList:
    :return:
    '''

    formatList = []
    if hasattr(objList, '__iter__'):
        for ele in objList:
            if not isinstance(ele, SPEC_TYPES) and hasattr(ele, '__iter__'):
                formatList.append(list_scanner(ele))
            else:
                if isinstance(ele, Vertex):
                    formatList.append(trans_vex(ele))
                elif isinstance(ele, Edge):
                    formatList.append(trans_edge(ele))
                elif isinstance(ele, PqueuePair):
                    formatList.append(str(ele))
                else:
                    formatList.append(ele)
    return formatList

def formatter(obj):
    '''
    format the output of single object
    :param obj:
    :return:
    '''
    #list type
    if isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
        return list(map(formatter, obj)) #this will add quotes to the elements
    elif isinstance(obj, dict):
        newDict = {}
        for key in obj:
            newDict[str(key)] = formatter(obj[key])
        return newDict
    elif isinstance(obj, Matrix):
        return formatter(obj.get_grid())
    elif isinstance(obj, BinaryMinHeap):
        return formatter(obj.elements)
    elif isinstance(obj, BinaryMaxHeap):
        return formatter(obj.elements)
    else:
        return str(obj)




