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



#my own bs
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


# copy paste:
# https://github.com/pucrs-automated-planning/pddl-parser/blob/master/PDDL.py
stack = []
outer_list = []

for char in test_splitted:
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



# nested_list_op.append(nested_list_op)
        #outer_list.append(nested_list_op)


#tokenize(test_splitted)

print("stack", stack)
print("outer_list", outer_list)
print("nested_list", nested_list)
#print("new_list", new_list)


print("stack_output")
while not stack_output.empty():
    print(stack_output.get(), end=" ")




