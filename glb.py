'''
Author: Fang Zhou
Date: 2015/5/6
Version: 1.0
Description: This file contains all the global variables which will be used in compiler.
'''

# store all the variables during the execution of pseudo code,
# Two types of elements stored in the stack:
# 1) module. Eg.: for module, function module...
# 2) variable. Format:
#    0         1           2                   3             4
#   [var name, var object, modification flag, [index list], [pointer, [index list of the pointer]]
#[var_name, variable_obj]
variable_stack = []

#store functions defined in pseudo code. {function name: function lambda} TODO not sure it should be function lambda or function module
function_map = {}
#store function module contents, also registered in function_map as a lambda function which will call function's __call__ method.
# function_module_map = {}

current_line = 0 #line of current statement, start from 0
contents = [] #pseudo code split by line breaks

step = 0 #indetifier of how many statements executed and printed
json_dict = {} #ouput json content stored inside this dictionary, key: statement_No, value: variables status
console_output = [] #store the console output

funcall_depth = 0 #current function call depth in function call tree

#used by the modification flag in variable stack
flag_dict = {
    "unchanged": 0,
    "new": 1,
    "changed": 2,
    "visited": 3,
}


DEFAULT_VERTEX_COLOR = 'gray'
DEFAULT_EDGE_COLOR = 'black'
VISITED_COLOR = 'yellow'

#range for generating random data structures
randomLowRange = 4
randomUpperRange = 7

task_queue = [] #use for multiple users


