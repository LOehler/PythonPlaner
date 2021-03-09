
from queue import LifoQueue
import re

# testing splitting
test = ("( and ( block a ) ( not ( on a b ) ) )") # ignore apostrophes bc pddl doesnt use them
print("test", test)
test.lower()  # lower can be used to make all chars lowercase (for later)
test_splitted = test.split()
print("test_splitted", test_splitted)

# testing stack
# stack = []
# Initializing a stack
stack = LifoQueue()
stack_output = LifoQueue()

outer_list = []

counter = 0

#my own bs for ref
"""for char in test_splitted:  # sublist
    # print(char)
  #  stack.put(char)
    if char != ')':
        stack.put(char)
        #counter += 1
        #print(counter)
    if char == ')':
        stack_output.put(nested_list_op)
        while not stack.empty():
            current = stack.get()  # LIFO
            if current in ["and", "not"]:  # check if operator
                #stack_output.put(current)
                #nested_list_op = []  # reset
              #  new_list = []
               # new_list.append(current)
                #nested_list_op.append(new_list)
                nested_list_op.append(current)  # -> operator will always be beginning of nested_list
                nested_list_op.append(nested_list_atoms[::-1])
                nested_list_atoms = []  # reset
                print("nested_list_op", nested_list_op)
                #outer_list.append(current)
            #    outer_list.append(nested_list_op)
            if current in ["block","on","a","b"]:  # check if atom
                nested_list_atoms.append(current)
                #print(nested_list_atoms)
            else:
                print("bruh")
                continue  # skip closing bracket
print("outer_list", outer_list)
print("nested_list", nested_list_atoms)"""

"""Hint: it is recommended to return a list of an action schemata representation, 
a dictionary mapping types to sets of constants for each type,
and the type hierarchy information. 
Take care to include an extra mapping from the type "" to a set of all objects. """

# copy paste:
# https://github.com/pucrs-automated-planning/pddl-parser/blob/master/PDDL.py


#  filename = "domain.pddl"
def tokenize(filename):

    with open(filename, 'r') as f:
        # TODO Remove single line comments

        # READ AND CLEAN
        str = f.read()
       # print(type(str))
       # print(str)

        str = str.lower()
        #str = str.split()

        # okay so i add spaces here so i can use split() later and its kinda clumsy but it works
        # adding spaces before and after brackets
        # maybe use str.split('( |) ')
        for ch in str:
            if ch == "(":
                str1 = str.replace("(", " ( ")
            elif ch == ")":
                str2 = str1.replace(")", " ) ")

        print("str", str2)

        str_splitted = str2.split()
        #print("str_splitted", str_splitted)

        # NEST LISTS FOR CORRECT TREE
        stack = []
        outer_list = []

        for char in str_splitted:
            if char == '(':
                stack.append(outer_list)
                outer_list = []  # reset
            elif char == ')':
                if stack :
                    nested_list = outer_list
                 #   print("nested_list", nested_list)
                    outer_list = stack.pop()
                  #  print("outer_list", outer_list)
                    outer_list.append(nested_list)
                else:
                    raise Exception('Missing open parentheses')
            else:
                outer_list.append(char)

        if stack:
            raise Exception('Missing close parentheses')
        if len(outer_list) != 1:
            raise Exception('Malformed expression')


    """
    print("outer_list", outer_list)
    print("nested_list", nested_list)
    print("stack_output")
    while not stack_output.empty():
        print(stack_output.get(), end=" ")"""

    return nested_list



#tokens = tokenize("domain.pddl")
tokens = tokenize("type_hierarchy_test.pddl")
print(tokens)


# TODO split in multiple functions for readability
def assign_types(list_tokens):

    # create dict
    # make keys
    for sub_list in list_tokens:
        if sub_list[0] == ":types":  # didnt clean list yet so idk where :types is and have to iterate over nested_list -> could be prettier?
            # both of the following work:
            # dict_types = {i: [] for i in sub_list[1:] }#and i != "-"}
            dict_types = dict.fromkeys(sub_list[1:], [])

            # TODO
            # cur problem: "-" is in dict bc it is in types
            # cannot delete dash bc we need it for hierarchy
            # just letting it in for now


    dict_types[""] = []  # if no dash

    # fill lists
    # example: sub_list[0] == ":constants" to test if assign types work

    print(list_tokens[2:])
    for sub_list in list_tokens[2:]:  # cut off ['define', ['domain', 'test-adl']

        # if sub_list[0] == ":types":
        sub_list = sub_list[1:]
        print("sub_list", sub_list)
        i = 0  # reset for each sublist
        stack = []

        for char in sub_list:
            #  print("sub_list for loop", sub_list)
            if char != '-':
                if sub_list[i - 1] == '-':  # check if char == key and skip
                    i += 1
                    # continue
                else:
                    stack.append(char)
                    i += 1
            # print("stack", stack)
            if char == '-':
                #  print("key", sub_list[i+1])  # = key
                if dict_types[sub_list[i + 1]]:  # list not empty -> key already has entries
                    dict_types[sub_list[i + 1]].append(  # append not overwrite
                        stack[0])  # stack[0] to get rid of nested list
                else:
                    dict_types[sub_list[i + 1]] = stack
                print("stack", stack)
                stack = []  # reset
                i += 1

        # check if key is entry of other key
        # = if key is a subtype
        # then copy all entries of subtype to other key
        for key_i in dict_types:
            for key_j in dict_types:
                if key_i in dict_types[key_j] and dict_types[key_i]:  # if key_i is a subtype AND already has entries
                    print("key_i", key_i)
                    print("key_j", key_j)

                    dict_types[key_j].remove(key_i)  # delete subtype in entry of type

                    list_to_copy = dict_types[key_i]  # copy entries of subtype
                    print("list to copy", list_to_copy)

                    # add to key_i
                    for item in list_to_copy:
                        dict_types[key_j].append(item)  # works

                    #  dict_types[key_j].append(list_to_copy)  # would work too but nested lists
                    continue
                else:
                    continue

        # no type assigned
        if "-" not in sub_list and sub_list[0] == ":types":
            dict_types[""] = sub_list

        # TODO fix duplicates in list (entries of keys)
    # idea 1: change lists to sets
    # idea 2: use sets from beginning

    # print("dict_types", dict_types)
    # return(dict_types)

    print("dict_types", dict_types)


assign_types(tokens)
#print(assign_types(tokens))




























