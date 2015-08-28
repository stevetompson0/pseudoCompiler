'''
Author: Fang Zhou
Date: 2015/5/7
Version: 1.0
Description: Main function. Load the pseudo code and submit for compilation
'''

import json, sys, os
import glb
import compilerSettings
from structure.config import *
from module.glbmodule import glbmodule


def pseudo(filepath, outputpath = None):
    with open(filepath, 'r') as infile:
        glb.contents = ''.join(infile.readlines()).split('\n') #to remove \n in each line

    #initialize globals and data structures into function list
    glb.function_map.update(globals())

    #initialize global settings
    glb.step = 1
    glb.funcall_depth = 0 #start from 0
    glb.variable_stack.clear()

    #start execution, line number start from 0
    init_module = glbmodule(glb.contents, line = 0)

    if not outputpath:
        # outputpath = 'output/output.json' #run locally
        outputpath = compilerSettings.jsonOutputPath

    try:
        init_module.run()
    except Exception as e:
        #write exception to a file
        with open(compilerSettings.exceptionPath, 'w') as f:
            #python 2.7 use e.message, python 3.3 use e.args, be careful
            f.write(str(e.args))
            f.close()

    #write variable information to JSON file
    with open(outputpath, 'w') as f:
        json.dump(glb.json_dict, f, sort_keys=True, indent=4)




if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3_command pseudo [filename] [optional: output path], recommended python version: 3.3')
        exit()
    if len(sys.argv) == 2:
        pseudo(sys.argv[1])
    if len(sys.argv) == 3:
        pseudo(sys.argv[1], sys.argv[2])