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
nested_list_atoms = []
nested_list_op = []
counter = 0

#def tokenize(test_list):

stack = []
outer_list = []

# copy paste:
# https://github.com/pucrs-automated-planning/pddl-parser/blob/master/PDDL.py
for char in test_splitted:
    if char == '(':
        stack.append(outer_list)
        outer_list = []  # reset
    elif char == ')':
        if stack:  # not empty
            nested_list = outer_list
            outer_list = stack.pop()
            outer_list.append(nested_list)
        else:
            raise Exception('Missing open parentheses')
    else:
        outer_list.append(char)

if stack:
    raise Exception('Missing close parentheses')
if len(outer_list) != 1:
    raise Exception('Malformed expression')



# nested_list_op.append(nested_list_op)
        #outer_list.append(nested_list_op)


#tokenize(test_splitted)

print("stack", stack)
print("list", outer_list[0])
print("nested_list_op", nested_list_op)
#print("new_list", new_list)


print("stack_output")
while not stack_output.empty():
    print(stack_output.get(), end=" ")




